from AsteriskRealtimeData.domain import pause_reason
from AsteriskRealtimeData.infrastructure.repositories.mongo.mongo_repository import (
    MongoRespository,
)
from antidote import inject, Provide
from AsteriskRealtimeData.domain.pause_reason.pause_reason import PauseReason
from AsteriskRealtimeData.domain.pause_reason.pause_reasons_vo import PauseReasonVo
from AsteriskRealtimeData.domain.pause_reason.pause_reason_created_vo import (
    PauseReasonCreatedVo,
)


class PauseReasonService:
    @inject
    def create_pause_reason(
        self, pause_reason_vo: PauseReasonVo, repository: Provide[MongoRespository]
    ) -> PauseReasonCreatedVo:

        pause_reason = PauseReason(
            pause_code=pause_reason_vo.pause_code,
            description=pause_reason_vo.description,
        )

        repository.save(
            "pause_reason", pause_reason, {"pause_code": pause_reason_vo.pause_code}
        )

        return PauseReasonCreatedVo(
            pause_code=pause_reason_vo.pause_code,
            description=pause_reason_vo.description,
        )

    @inject()
    def list_pause_reason(
        self, repository: Provide[MongoRespository]
    ) -> list[PauseReasonVo]:
        result: list = []
        for document in repository.list("pause_reason"):
            result.append(
                PauseReasonVo(
                    pause_code=document["pause_code"],
                    description=document["description"],
                )
            )
        return result

    @inject
    def get_pause_reason(
        self, id: str, repository: Provide[MongoRespository]
    ) -> PauseReasonVo:
        pause_reason = repository.get_by_id("pause_reason", {"pause_code": id})
        return PauseReasonVo(
            pause_code=pause_reason["pause_code"],
            description=pause_reason["description"],
        )

    @inject
    def delete_pause_reason(
        self, id: str, repository: Provide[MongoRespository]
    ) -> PauseReasonVo:
        pause_reason = repository.delete_by_id("pause_reason", {"pause_code": id})
        print(type(pause_reason))
        print(pause_reason.deleted_count)
