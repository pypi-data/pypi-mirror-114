import asyncio
import inspect
import logging
import uuid

from endpointlib.clients.mqtt_async_client import MQTTAsyncClient
from endpointlib.devices.device import Device
from endpointlib.endpoints.endpoint_device import EndpointDevice

logger = logging.getLogger('endpointlib')

class EndpointMonitorDevice(EndpointDevice):
    def __init__(self, host: str, port: int, device: Device, monitor_device: Device, delay: float, command: str, on_monitor_callback=None, main_callback=None, handlers=None) -> None:
        super().__init__(host, port, device=device, main_callback=main_callback, handlers=handlers)
        self._monitor_device = monitor_device
        self._delay = delay
        self._command = command
        self._on_monitor = on_monitor_callback

    async def run_monitor(self):
        async with MQTTAsyncClient(id=self._generate_id(), host=self.host, port=self.port) as client:
            await client.connect()
            while True:
                status = await self._monitor_device.send_command(self._command)
                try:
                    # If callback defined then runit else run on_monitor for inheritors
                    if self._on_monitor:
                        if inspect.iscoroutinefunction(self._on_monitor):
                            params = len(inspect.signature(self._on_monitor).parameters)
                            if (params == 2):
                                await self._on_monitor(status, client)
                            elif (params == 3):
                                dev = self.get_device()
                                await self._on_monitor(status, dev, client)
                        else:
                            await asyncio.get_event_loop().run_in_executor(None, self._on_monitor, status)
                    else:
                        dev = self.get_device()
                        await self.on_monitor(status, dev, client)
                except Exception as ex:
                    logger.error(str(ex))

                await asyncio.sleep(delay=self._delay)

    def _generate_id(self) -> str:
        return str(uuid.uuid4())

    async def on_monitor(self, status: str, device:Device, client: MQTTAsyncClient):
        pass

    def get_routines(self):
        tasks =  super().get_routines()
        tasks.append(self.run_monitor())
        return tasks
