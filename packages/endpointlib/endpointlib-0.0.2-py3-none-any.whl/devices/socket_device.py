from endpointlib.connections.socket_connection import SocketConnection
from endpointlib.devices.device import Device

class SocketDevice(Device):
    def __init__(self, host: str, port: int) -> None:
        super().__init__(SocketConnection(host, port))
