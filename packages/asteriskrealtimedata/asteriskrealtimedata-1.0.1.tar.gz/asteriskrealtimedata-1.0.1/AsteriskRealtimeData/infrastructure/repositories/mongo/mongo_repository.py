from AsteriskRealtimeData.domain.entity import Entity
from AsteriskRealtimeData.domain.pause_reason.pause_reason import PauseReason
from antidote import service, Provide, inject

from AsteriskRealtimeData.infrastructure.repositories.mongo.mongo_connection import (
    MongoConnection,
)
from AsteriskRealtimeData.infrastructure.repositories.repository_interface import (
    Repository,
)


@service(singleton=True)
class MongoRespository(Repository):
    @inject
    def __init__(self, connection: Provide[MongoConnection]) -> None:
        self.connection = connection

    def save(
        self,
        table_name: str,
        entity: Entity,
        identify_field: dict,
    ):
        table = self.connection.get_connection()[table_name]
        return table.replace_one(
            identify_field,
            entity.as_dict(),
            upsert=True,
        )

    def list(self, table_name: str):
        table = self.connection.get_connection()[table_name]
        return table.find({})

    def get_by_id(self, table_name: str, search: dict):
        table = self.connection.get_connection()[table_name]
        return table.find_one(search)

    def delete_by_id(self, table_name: str, search: dict):
        table = self.connection.get_connection()[table_name]
        return table.delete_one(search)
