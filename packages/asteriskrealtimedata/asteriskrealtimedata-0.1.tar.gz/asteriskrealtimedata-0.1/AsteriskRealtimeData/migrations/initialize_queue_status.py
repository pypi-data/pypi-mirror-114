from AsteriskRealtimeData.infrastructure.repositories.mongo.mongo_connection import (
    MongoConnection,
)
from AsteriskRealtimeData.asterisk_informations import AsteriskInformations
from AsteriskRealtimeData.domain.queue_status.queue_status import QueueStatus


class InitializePauseReasons:
    def __init__(self) -> None:
        self.asterisk_informations = AsteriskInformations(MongoConnection())

    def initialize_queue_status(self):
        self.asterisk_informations.insert_or_update_queue_status(
            queue_status=QueueStatus(0, "Desconocido")
        )
        self.asterisk_informations.insert_or_update_queue_status(
            queue_status=QueueStatus(1, "Sin Uso")
        )
        self.asterisk_informations.insert_or_update_queue_status(
            queue_status=QueueStatus(2, "Hablando")
        )
        self.asterisk_informations.insert_or_update_queue_status(
            queue_status=QueueStatus(3, "Ocupado")
        )
        self.asterisk_informations.insert_or_update_queue_status(
            queue_status=QueueStatus(4, "Invalido")
        )
        self.asterisk_informations.insert_or_update_queue_status(
            queue_status=QueueStatus(5, "Indisponible")
        )
        self.asterisk_informations.insert_or_update_queue_status(
            queue_status=QueueStatus(6, "Ringing")
        )
        self.asterisk_informations.insert_or_update_queue_status(
            queue_status=QueueStatus(7, "RingInUse")
        )
        self.asterisk_informations.insert_or_update_queue_status(
            queue_status=QueueStatus(8, "En Espera")
        )
        self.asterisk_informations.insert_or_update_queue_status(
            queue_status=QueueStatus(9, "Cortando")
        )


InitializePauseReasons().initialize_queue_status()
