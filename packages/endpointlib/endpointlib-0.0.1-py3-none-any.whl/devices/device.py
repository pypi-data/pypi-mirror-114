import asyncio
import logging

from endpointlib.connections.connection import Connection

logger = logging.getLogger('endpointlib')

class Device:
    def __init__(self, connection: Connection) -> None:
        self._connection = connection

    async def send_command(self, command: str) -> str:
        try:
            await self._connection.connect()
            try:
                raw = await self._connection.send_string(command)
            finally:
                await self._connection.disconnect()
            return self.process_response(raw)
        except Exception as ex:
            logger.error(str(ex))
        return self.no_response()

    # In case someone needs to process the response and return
    # something else then inherit this method
    def process_response(self, raw: str) -> str:
        return raw
    
    # If someone needs to return other str than None then inherit
    # this method
    def no_response(self) -> str:
        return None
