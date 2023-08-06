import asyncio
import inspect
import logging
import uuid

from endpointlib.clients.mqtt_async_client import MQTTAsyncClient

logger = logging.getLogger('endpointlib')

class Endpoint:
    def __init__(self, host: str, port: int, main_callback=None, handlers=None) -> None:
        if (handlers is None):
            handlers = dict()
        self.id = str(uuid.uuid4())
        self.host = host
        self.port = port
        self._main_callback = main_callback
        self._handlers = handlers
        self._command_handlers = dict()

    def get_id(self) -> str:
        return self._id
    
    def create_id(self) -> str:
        return str(uuid.uuid4())

    async def run_forever(self) -> None:
        try:
            tasks = self.get_routines()
            await asyncio.gather(*tasks)
        except Exception as ex:
            logger.error(str(ex))

    def get_routines(self):
        tasks = []
        tasks.append(self.run_mqtt_client())
        tasks.append(self._main_wrapper())
        return tasks

    async def run_mqtt_client(self):
        async with MQTTAsyncClient(id=self.id, host=self.host, port=self.port) as client:
            await client.connect()
            self.setup_process_message(client=client)
            await self._setup_command_handlers(client)
            await client.loop_forever()

    def get_handlers(self) -> dict:
        return dict()

    def get_command_handlers(self) -> dict:
        return self._command_handlers

    def setup_process_message(self, client: MQTTAsyncClient):
        client.process_message = self._process_message

    async def _main_wrapper(self):
        async with MQTTAsyncClient(id=self.create_id(), host=self.host, port=self.port) as client:
            await client.connect()
            if (self._main_callback):
                await self._main_callback(client)
            else:
                await self.on_main(client)

    async def on_main(self, client: MQTTAsyncClient):
        pass

    async def _setup_command_handlers(self, client: MQTTAsyncClient):
        topics = set()
        if (not self._handlers):
            for k, v in self.get_handlers().items():
                self._command_handlers[k] = v
                topics.add(k)
        else:
            for k, v in self._handlers.items():
                self._command_handlers[k] = v
                topics.add(k)
        await client.subscribe(topics)

    async def _process_message(self, topic, payload):
        handler = self._command_handlers.get(topic, None)
        if (handler is not None):
            if inspect.iscoroutinefunction(handler):
                params = len(inspect.signature(handler).parameters)
                if (params == 2):
                    await handler(topic, payload)
                elif (params == 3):
                    async with MQTTAsyncClient(id=self.create_id(), host=self.host, port=self.port) as client:
                        await client.connect()
                        await handler(topic, payload, client)
            else:
                   await asyncio.get_event_loop().run_in_executor(None, handler, topic, payload)
