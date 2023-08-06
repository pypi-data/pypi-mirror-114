import asyncio
import logging

from endpointlib.connections.connection import Connection

logger = logging.getLogger('endpointlib')

class SocketConnection(Connection):
    def __init__(self, host: str, port: int) -> None:
        super().__init__()
        self._host = host
        self._port = port
        self._reader = None
        self._writer = None
    
    def is_connected(self) -> bool:
        if (self._reader is not None and self._writer is not None):
            if (not self._writer.is_closing()):
                return True
        return False

    async def connect(self):
        try:           
            self._reader, self._writer = await asyncio.open_connection(
                    self._host, self._port)
        except Exception as ex:
            logger.error(str(ex))
    
    async def send(self, data: bytes) -> bytes:
        response = None
        if (self.is_connected()):
            try:
                self._writer.write(data)
                await self._writer.drain()
                response = await self._reader.read(2048)
            except Exception as ex:
                logger.error(str(ex))
        return response

    async def disconnect(self):
        if (self.is_connected()):
            self._writer.close()
            await self._writer.wait_closed()
        self._reader = None
        self._writer = None
