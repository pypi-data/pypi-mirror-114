from endpointlib.connections.serial_connection import SerialConnection
from endpointlib.devices.device import Device

class SerialDevice(Device):
    def __init__(self, port: str, baudrate: int) -> None:
        super().__init__(SerialConnection(port=port, baudrate=baudrate))