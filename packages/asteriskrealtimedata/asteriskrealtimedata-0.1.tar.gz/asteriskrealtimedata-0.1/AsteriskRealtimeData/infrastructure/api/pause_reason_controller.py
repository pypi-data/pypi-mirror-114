from AsteriskRealtimeData.application.pause_reasons_service import PauseReasonService
from AsteriskRealtimeData.domain.pause_reason import pause_reason_created_vo
from AsteriskRealtimeData.domain.pause_reason.pause_reasons_vo import PauseReasonVo
from AsteriskRealtimeData.domain.pause_reason.pause_reason_created_vo import (
    PauseReasonCreatedVo,
)


class PauseReasonController:
    def create(self, pause_reason: PauseReasonVo) -> PauseReasonCreatedVo:
        pause_reason_parameter = PauseReasonVo(**pause_reason)
        return PauseReasonService().create_pause_reason(pause_reason_parameter)

    def list(self) -> list[dict]:
        pause_reasons = PauseReasonService().list_pause_reason()
        result: list = []

        for pause_reason in pause_reasons:
            result.append(pause_reason.as_dict())

        return result

    def get_by_id(self, id: str) -> dict:
        return PauseReasonService().get_pause_reason(id).as_dict()

    def delete_by_id(self, id: str) -> dict:
        return PauseReasonService().delete_pause_reason(id)
