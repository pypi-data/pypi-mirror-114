# sources: controller/service.proto
# plugin: python-betterproto
from dataclasses import dataclass

import betterproto

from ..models import controller


@dataclass
class ExecuteEncryptedControllerJobRequest(betterproto.Message):
    job: controller.EncryptedControllerJob = betterproto.message_field(1)


@dataclass
class ExecuteEncryptedControllerJobResponse(betterproto.Message):
    job_id: str = betterproto.string_field(1)


@dataclass
class GetControllerJobResultsRequest(betterproto.Message):
    job_id: str = betterproto.string_field(1)


@dataclass
class GetControllerJobResultsResponse(betterproto.Message):
    result: controller.ControllerJobExecutionResult = betterproto.message_field(1)
