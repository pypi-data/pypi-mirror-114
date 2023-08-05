# sources: translation/service.proto
# plugin: python-betterproto
from dataclasses import dataclass

import betterproto
from ..models import controller


@dataclass
class TranslateQuilToEncryptedControllerJobRequest(betterproto.Message):
    quantum_processor_id: str = betterproto.string_field(1)
    quil_program: str = betterproto.string_field(2)
    num_shots_value: int = betterproto.uint32_field(3, group="num_shots")


@dataclass
class TranslateQuilToEncryptedControllerJobResponse(betterproto.Message):
    job: controller.EncryptedControllerJob = betterproto.message_field(1)
