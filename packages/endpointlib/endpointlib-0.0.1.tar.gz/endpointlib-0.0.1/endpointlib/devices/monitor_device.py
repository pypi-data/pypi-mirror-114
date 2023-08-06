import asyncio
import logging
import inspect

from endpointlib.connections.connection import Connection
from endpointlib.devices.device import Device

logger = logging.getLogger('endpointlib')

class MonitorDevice(Device):
    def __init__(self, connection: Connection, command: str, delay: float, callback) -> None:
        super().__init__(connection)
        self._command = command
        self._delay = delay
        self._callback = callback

    async def run_monitor(self):
        while True:           
            status = await self.send_command(self._command)
            try:
                # If callback defined then runit else run on_monitor for inheritors
                if self._callback:
                    if inspect.iscoroutinefunction(self._callback):
                        await self._callback(status)
                    else:
                        await asyncio.get_event_loop().run_in_executor(None, self._callback(status))
                else:
                    await self.on_monitor(status)
                await asyncio.sleep(delay=self._delay)
            except Exception as ex:
                logger.error(str(ex))

    async def on_monitor(self, status):
        pass
