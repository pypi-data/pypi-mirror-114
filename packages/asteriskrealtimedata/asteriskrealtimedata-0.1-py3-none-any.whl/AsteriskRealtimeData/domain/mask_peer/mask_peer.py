from AsteriskRealtimeData.shared.decorators.entity import Entity


@Entity("mask_peer")
class MaskPeer:
    _peer_ip_address: str

    def __init__(self, peer_ip_address):
        self._peer_ip_address = peer_ip_address

    def get_peer_ip_address(self) -> str:
        return self._peer_ip_address

    def as_dict(self):
        return self.__repr__()

    def __repr__(self):
        return {"ipaddress": self.get_peer_ip_address()}
