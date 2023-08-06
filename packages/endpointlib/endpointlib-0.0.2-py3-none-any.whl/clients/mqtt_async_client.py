import asyncio
import logging

from types import TracebackType
from typing import Type

from asyncio_mqtt import Client, MqttError, MqttCodeError
from contextlib import AsyncExitStack

logger = logging.getLogger('endpointlib')

class MQTTAsyncClient(AsyncExitStack):
    def __init__(self, id: str, host: str, port: int) -> None:
        super().__init__()
        self._host = host
        self._port = port
        self._id = id
        self._client = None
        self._stack = None
        self._tasks = set()
        self._process_message = lambda *xargs: None

    @property
    def process_message(self):
        return self._process_message

    @process_message.setter
    def process_message(self, value):
        self._process_message = value

    def is_connected(self):
        return self._client is not None

    async def connect(self):
        if (self.is_connected()): return
        self.push_async_callback(self._cancel_tasks, self._tasks)

        self._client = Client(client_id=self._id, hostname=self._host, port=self._port)
        await self.enter_async_context(self._client)

    async def publish(self, topic: str, payload: str, qos=0, retain=False):
        try:
            await self._client.publish(topic=topic, payload=payload, qos=qos, retain=retain)
        except MqttError as merr:
            logger.error(str(merr))
        except MqttCodeError as cerr:
            logger.error(str(cerr))
        except Exception as ex:
            logger.error(str(ex))

    async def subscribe(self, topics):
        if (self.is_connected()):
            for topic in topics:
                manager = self._client.filtered_messages(topic_filter=topic)
                messages = await self.enter_async_context(manager)
                task = asyncio.create_task(self._process_messages(messages))
                self._tasks.add(task)

            for topic in topics:
                await self._client.subscribe(topic)

    async def loop_forever(self):
        if (self.is_connected()):
            reconnect_interval = 3
            while True:
                try:
                    await asyncio.gather(*self._tasks)
                    await asyncio.sleep(1)
                except MqttError as error:
                    logger.error(str(error))
                finally:
                    await asyncio.sleep(reconnect_interval)

    async def _process_messages(self, messages):
        async for message in messages:
            # Safe Invoke
            try:
                await self.process_message(message.topic, message.payload.decode('utf-8'))
            except Exception as ex:
                logger.error(str(ex))

    async def _cancel_tasks(self, tasks):
        for task in tasks:
            if task.done():
                continue
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass
