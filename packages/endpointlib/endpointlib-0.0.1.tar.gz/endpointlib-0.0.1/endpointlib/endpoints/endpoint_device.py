import asyncio
import inspect

from endpointlib.clients.mqtt_async_client import MQTTAsyncClient
from endpointlib.devices.device import Device
from endpointlib.endpoints.endpoint import Endpoint

class EndpointDevice(Endpoint):
    def __init__(self, host: str, port: int, device: Device, main_callback=None, handlers=None) -> None:
        super().__init__(host, port, main_callback=main_callback, handlers=handlers)
        self._device = device

    def get_device(self):
        return self._device

    def setup_process_message(self, client: MQTTAsyncClient):
        client.process_message = self._process_message_device

    async def _process_message_device(self, topic, payload):
        handler = self.get_command_handlers().get(topic, None)
        if (handler is not None):
            if inspect.iscoroutinefunction(handler):
                params = len(inspect.signature(handler).parameters)
                if (params == 2):
                    await handler(topic, payload)
                elif (params == 3):
                    await handler(topic, payload, self._device)
                elif (params == 4):
                    async with MQTTAsyncClient(id=self.create_id(), host=self.host, port=self.port) as client:
                        await client.connect()
                        await handler(topic, payload, self._device, client)
            else:
                await asyncio.get_event_loop().run_in_executor(None, handler, topic, payload)
