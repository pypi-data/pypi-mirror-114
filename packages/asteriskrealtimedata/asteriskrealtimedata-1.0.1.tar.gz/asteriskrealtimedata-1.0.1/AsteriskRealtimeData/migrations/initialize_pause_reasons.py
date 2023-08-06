from AsteriskRealtimeData.infrastructure.repositories.mongo.mongo_connection import (
    MongoConnection,
)
from AsteriskRealtimeData.asterisk_informations import AsteriskInformations
from AsteriskRealtimeData.domain.pause_reason.pause_reason import PauseReason


class InitializePauseReasons:
    def __init__(self) -> None:
        self.asterisk_informations = AsteriskInformations(MongoConnection())

    def initialize_pause_reasons(self):
        self.asterisk_informations.insert_or_update_pause_reason(
            pause_reason=PauseReason("100001", "Conectado")
        )
        self.asterisk_informations.insert_or_update_pause_reason(
            pause_reason=PauseReason("100002", "Disponible")
        )
        self.asterisk_informations.insert_or_update_pause_reason(
            pause_reason=PauseReason("200001", "Desconectado")
        )
        self.asterisk_informations.insert_or_update_pause_reason(
            pause_reason=PauseReason("200002", "En colación")
        )
        self.asterisk_informations.insert_or_update_pause_reason(
            pause_reason=PauseReason("200003", "Baño")
        )
        self.asterisk_informations.insert_or_update_pause_reason(
            pause_reason=PauseReason("200004", "En Reunión")
        )
        self.asterisk_informations.insert_or_update_pause_reason(
            pause_reason=PauseReason("200005", "Atención vendedor")
        )
        self.asterisk_informations.insert_or_update_pause_reason(
            pause_reason=PauseReason("300001", "Hablando")
        )
        self.asterisk_informations.insert_or_update_pause_reason(
            pause_reason=PauseReason("300002", "ACW (After Call Work)")
        )
        self.asterisk_informations.insert_or_update_pause_reason(
            pause_reason=PauseReason("300003", "Ocupado")
        )
        self.asterisk_informations.insert_or_update_pause_reason(
            pause_reason=PauseReason("300004", "Recibiendo llamada")
        )
        self.asterisk_informations.insert_or_update_pause_reason(
            pause_reason=PauseReason("300005", "Discando")
        )
        self.asterisk_informations.insert_or_update_pause_reason(
            pause_reason=PauseReason("000000", "Estado desconocido")
        )


InitializePauseReasons().initialize_pause_reasons()
