import abc
from typing import TYPE_CHECKING, Any, Optional, Type, TypeVar
from urllib.parse import urlparse

import grpclib
from grpclib.client import Channel, Stream
from qcs_api_client.client._configuration.configuration import QCSClientConfiguration
from qcs_api_client.client.auth import QCSAuth
from qcs_api_client.grpc import models
from qcs_api_client.grpc.services import controller, translation

if TYPE_CHECKING:
    from grpclib._typing import IProtoMessage


T = TypeVar("T")

DEFAULT_PORTS = {"http": 80, "https": 443}


class Client(abc.ABC):
    """
    Base class for async gRPC service stubs.
    """

    _auth_handler: QCSAuth
    _channel: Channel
    timeout: Optional[float]

    def __init__(
        self,
        *,
        auth_handler: Optional[QCSAuth] = None,
        channel: Optional["Channel"] = None,
        timeout: Optional[float] = None,
        url: Optional[str] = None,
    ) -> None:
        self._auth_handler = auth_handler or QCSAuth(client_configuration=QCSClientConfiguration.load())
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
            self._channel = Channel(host=parsed.hostname, port=parsed.port, ssl=parsed.scheme == "https")
        else:
            self._channel = channel

        self.timeout = timeout

    def __resolve_request_kwargs(
        self,
        timeout: Optional[float],
    ):
        metadata = {}

        if (
            self._auth_handler._auth_configuration.pre
            and self._auth_handler._client_configuration.credentials.token_payload.should_refresh()
        ):
            self._auth_handler.sync_refresh_token()

        metadata["authorization"] = f"Bearer {self._auth_handler._client_configuration.credentials.access_token}"

        return {"timeout": self.timeout if timeout is None else timeout, "metadata": metadata}

    async def _unary_unary(
        self,
        *,
        route: str,
        request: "IProtoMessage",
        response_type: Type[T],
        retry_on_auth_failure: bool = True,
        timeout: Optional[float] = None,
    ) -> T:
        """Make a unary request and return the response."""
        try:
            async with self._channel.request(
                route,
                grpclib.const.Cardinality.UNARY_UNARY,
                type(request),
                response_type,
                **self.__resolve_request_kwargs(timeout),
            ) as stream:
                response = await _send_request_on_stream(stream=stream, request=request)

        except Exception as e:
            if retry_on_auth_failure is True:
                self._auth_handler.sync_refresh_token()
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

    def close(self):
        self._channel.close()

    async def translate_quil_to_encrypted_controller_job(
        self, *, quantum_processor_id: str, quil_program: str, num_shots: Optional[int] = 0
    ) -> translation.TranslateQuilToEncryptedControllerJobResponse:
        request = translation.TranslateQuilToEncryptedControllerJobRequest()
        request.quantum_processor_id = quantum_processor_id
        request.quil_program = quil_program
        request.num_shots_value = num_shots

        return await self._unary_unary(
            route="/services.translation.Translation/TranslateQuilToEncryptedControllerJob",
            request=request,
            response_type=translation.TranslateQuilToEncryptedControllerJobResponse,
        )

    async def execute_encrypted_controller_job(
        self, *, job: Optional[models.controller.EncryptedControllerJob] = None
    ) -> controller.ExecuteEncryptedControllerJobResponse:
        request = controller.ExecuteEncryptedControllerJobRequest()
        if job is not None:
            request.job = job

        return await self._unary_unary(
            "/services.controller.Controller/ExecuteEncryptedControllerJob",
            request,
            controller.ExecuteEncryptedControllerJobResponse,
        )

    async def get_controller_job_results(self, *, job_id: str = "") -> controller.GetControllerJobResultsResponse:
        request = controller.GetControllerJobResultsRequest()
        request.job_id = job_id

        return await self._unary_unary(
            "/services.controller.Controller/GetControllerJobResults",
            request,
            controller.GetControllerJobResultsResponse,
        )


async def _send_request_on_stream(*, stream: Stream, request: "IProtoMessage") -> Any:
    """
    Given a request and a stream, asynchronously send the request on that stream.
    """
    await stream.send_message(request, end=True)
    response = await stream.recv_message()
    assert response is not None

    return response
