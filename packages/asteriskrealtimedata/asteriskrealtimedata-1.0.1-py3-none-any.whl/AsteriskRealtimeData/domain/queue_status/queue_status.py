from AsteriskRealtimeData.shared.decorators.entity import Entity


@Entity("queue_status")
class QueueStatus:
    status_code: int
    description: str

    def __init__(self, status_code: int, description: str):
        self.status_code = status_code
        self.description = description

    def get_status_code(self) -> int:
        return self.status_code

    def get_description(self) -> str:
        return self.description

    def as_dict(self) -> dict:
        return self.__repr__()

    def __repr__(self):
        return {
            "status_code": self.get_status_code(),
            "description": self.get_description(),
        }
