from AsteriskRealtimeData.domain.entity import Entity
from dataclasses import dataclass
from uuid import UUID, uuid4


@dataclass
class PauseReason(Entity):
    id: UUID = uuid4()
    pause_code: str = "000000"
    description: str = "Sin estado"

    def get_pause_code(self) -> str:
        return self.pause_code

    def get_description(self) -> str:
        return self.description

    def as_dict(self) -> dict:
        return self.__repr__()

    def __repr__(self):
        return {
            "pause_code": self.get_pause_code(),
            "description": self.get_description(),
        }
