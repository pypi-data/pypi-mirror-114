from AsteriskRealtimeData.shared.decorators.entity import Entity


@Entity("peers")
class Peer:
    _peer_name: str
    _peer_type: str
    _peer_ip_address: str

    def __init__(self, peer_name, peer_type, peer_ip_address):
        self._peer_name = peer_name
        self._peer_type = peer_type
        self._peer_ip_address = peer_ip_address

    def get_peer_name(self) -> str:
        return self._peer_name

    def get_peer_type(self) -> str:
        return self._peer_type

    def get_peer_ip_address(self) -> str:
        return self._peer_ip_address

    def as_dict(self):
        return self.__repr__()

    def __repr__(self):
        return {
            "peer": self.get_peer_name(),
            "type": self.get_peer_type(),
            "ipaddress": self.get_peer_ip_address(),
        }
