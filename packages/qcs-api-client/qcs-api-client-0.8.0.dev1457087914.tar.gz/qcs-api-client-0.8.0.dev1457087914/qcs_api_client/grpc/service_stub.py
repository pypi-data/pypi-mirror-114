from typing import TYPE_CHECKING, Any, Optional, Type, TypeVar
from urllib.parse import urlparse

import grpclib
from grpclib.client import Channel, Stream
from grpclib.const import Status
from qcs_api_client.client._configuration.configuration import QCSClientConfiguration
from qcs_api_client.client.auth import QCSAuth

if TYPE_CHECKING:
    from grpclib._typing import IProtoMessage


T = TypeVar("T")

DEFAULT_PORTS = {"http": 80, "https": 443}


class ServiceStub:
    """
    A service stub pre-configured for calls to QCS gRPC services. Replaces ``betterproto.ServiceStub``.

    * Uses QCS-standard authentication & configuration files
    * Refreshes authorization tokens after "unauthenticated" responses received from service endpoints
    """

    _auth_handler: QCSAuth
    _channel: Channel
    timeout: Optional[float]

    def __init__(
        self,
        *,
        auth_handler: Optional[QCSAuth] = None,
        client_configuration: Optional[QCSClientConfiguration] = None,
        channel: Optional["Channel"] = None,
        timeout: Optional[float] = None,
        url: Optional[str] = None,
    ) -> None:
        self._auth_handler = auth_handler or QCSAuth(
            client_configuration=client_configuration or QCSClientConfiguration.load()
        )
        if (channel is None and url is None) or (channel is not None and url is not None):
            raise ValueError("exactly one of `channel` or `url` must be provided")

        if channel is None:
            parsed = urlparse(url)
            assert parsed.hostname is not None, "url must include service hostname"
            if parsed.port is None:
                port = DEFAULT_PORTS.get(parsed.scheme)
            else:
                port = parsed.port
            assert port is not None, "url must include service port"
            self._channel = Channel(host=parsed.hostname, port=port, ssl=parsed.scheme == "https")
        else:
            self._channel = channel

        self.timeout = timeout

    def __del__(self):
        """
        Close the channel on object destruction.
        """
        try:
            self._channel.close()
        except Exception:
            pass

    async def __resolve_request_kwargs(
        self,
        timeout: Optional[float],
    ):
        """
        Yield authorization header for request metadata.
        """
        metadata = {}

        if (
            self._auth_handler._auth_configuration.pre
            and self._auth_handler._client_configuration.credentials.token_payload.should_refresh()
        ):
            await self._auth_handler.async_refresh_token()

        token = self._auth_handler._client_configuration.credentials.access_token

        if token is not None:
            metadata["authorization"] = f"Bearer {token}"

        return {"timeout": self.timeout if timeout is None else timeout, "metadata": metadata}

    async def _unary_unary(
        self,
        route: str,
        request: "IProtoMessage",
        response_type: Type[T],
        *,
        retry_on_auth_failure: bool = True,
        timeout: Optional[float] = None,
        **kwargs,
    ) -> T:
        """Make a unary request and return the response."""
        try:
            async with self._channel.request(
                route,
                grpclib.const.Cardinality.UNARY_UNARY,
                type(request),
                response_type,
                **await self.__resolve_request_kwargs(timeout),
            ) as stream:
                response = await _send_request_on_stream(stream=stream, request=request)

        except Exception as e:
            if retry_on_auth_failure is True and getattr(e, "status", None) == Status.UNAUTHENTICATED:
                await self._auth_handler.async_refresh_token()
                return await self._unary_unary(
                    route=route,
                    request=request,
                    response_type=response_type,
                    retry_on_auth_failure=False,
                    timeout=timeout,
                )
            else:
                raise e from None

        return response


async def _send_request_on_stream(*, stream: Stream, request: "IProtoMessage") -> Any:
    """
    Given a request and a stream, asynchronously send the request on that stream.
    """
    await stream.send_message(request, end=True)
    response = await stream.recv_message()
    assert response is not None

    return response
