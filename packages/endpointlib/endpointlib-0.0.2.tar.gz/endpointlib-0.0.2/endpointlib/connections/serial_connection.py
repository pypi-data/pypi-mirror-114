import asyncio
import logging
import serial_asyncio

from endpointlib.connections.connection import Connection

class SerialConnection(Connection):
    def __init__(self, port: str, baudrate: int) -> None:
        super().__init__()
        self._port = port
        self._baudrate = baudrate
        self._reader = None
        self._writer = None
        self._logger = logging.getLogger('endpointlib')
    
    def is_connected(self) -> bool:
        if (self._reader is not None and self._writer is not None):
            if (not self._writer.is_closing()):
                return True
        return False
    
    async def connect(self):
        try:
            self._reader, self._writer = await serial_asyncio.open_serial_connection(
                url=self._port, baudrate=self._baudrate)
        except Exception as ex:
            self._logger.error(str(ex))
    
    async def send(self, data: bytes) -> bytes:
        response = None
        if (self.is_connected()):
            try:
                self._writer.write(data)
                await self._writer.drain()
                response = await self._reader.read(2048)
            except Exception as ex:
                self._logger.error(str(ex))
        return response
    
    async def disconnect(self):
        if (self.is_connected()):
            self._writer.close()
            await self._writer.wait_closed()
        self._reader = None
        self._writer = None
