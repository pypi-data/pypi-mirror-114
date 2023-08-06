"""
Module providing helpers to deal with RabbitMQ
"""

from typing import Any, Awaitable, Callable, Dict, Union, TypedDict
import asyncio

import aio_pika
from aiostream.stream import zip as aio_zip
from aiostream.stream import merge as aio_merge
from aiostream.stream import repeat as aio_repeat


class ConnectionParameters(TypedDict):
    """Class holding aio_pika's robust connection infos"""
    login: str
    password: str
    host: str
    port: int
    virtual_host: str
    ssl: bool
    ssl_options: Dict

class AsyncConsumerPublisherChannel:
    def __init__(
            self,
            connection: aio_pika.connection.Connection,
            channel: aio_pika.channel.Channel,
    ):
        self._connection = connection
        self._channel = channel
        self._consumers: Dict[str, Dict[str: Any[Callable, aio_pika.queue.Queue]]] = {}
        self._publishers: Dict[str, aio_pika.exchange.Exchange] = {}

    async def configure_consumer(self, queue_name: str, callback: Callable, name = None):
        """Add and configure a consumer"""
        name = name or queue_name
        queue = await self._channel.declare_queue(name=queue_name, durable=True, passive=True)
        self._consumers[name] = {
            "queue": queue,
            "callback": callback,
        }

    async def consume(self, name):
        async with self._consumers[name]["queue"].iterator() as queue_iter:
            try:
                async for message in queue_iter:
                    incoming_routing_key = message.info()["routing_key"]
                    async with message.process():
                        await self._consumers[name]["callback"](body=message.body, incomming_routing_key=incoming_routing_key)
            except asyncio.CancelledError:
                pass

    async def consume_all(self):
        merged_consumers_iterators = aio_merge(*[aio_zip(aio_repeat(consumer["callback"]), consumer["queue"].iterator())
                                       for _, consumer in self._consumers.items()])
        async with merged_consumers_iterators.stream() as consumers_iterator:
                try:
                    async for callback, message in consumers_iterator:
                        incoming_routing_key = message.info()["routing_key"]
                        async with message.process():
                            await callback(body=message.body, incoming_routing_key=incoming_routing_key)
                except asyncio.CancelledError:
                    pass

    async def configure_publisher(self, exchange_name: str, name=None):
        """Add and configure a publisher"""
        name = name or exchange_name
        exchange = await self._channel.declare_exchange(name=exchange_name, type='topic', durable=True, passive=True)
        self._publishers[name] = exchange

    async def publish(self, name: str, routing_key: str, message_body: str):
        message = aio_pika.Message(body=message_body.encode())
        await self._publishers[name].publish(message, routing_key=routing_key)

    async def close(self):
        await self._channel.close()


class AsyncRMQSession:
    def __init__(self):
        self._connection: aio_pika.connection.Connection = None
        self._channels: Dict[str, AsyncConsumerPublisherChannel] = {}

    async def connect(
            self,
            connection_params: ConnectionParameters,
            loop: asyncio.events.AbstractEventLoop=None,
            timeout: Union[int, float]=None,
            reconnect_interval: int=5,
            fail_fast: bool=1, # must be an int, as the argument is directly passed to yarl.URL.build querry args and doesn't accept bool types
    ):
        if self._connection is not None:
            return
        self._connection = await aio_pika.connect_robust(**connection_params,
                                                        timeout=timeout,
                                                        reconnect_interval=reconnect_interval,
                                                        fail_fast=fail_fast,
                                                        loop=loop)

    async def configure_channel(
            self,
            name,
            configure_channel: Callable[[AsyncConsumerPublisherChannel], Awaitable[None]]
    ) -> AsyncConsumerPublisherChannel:
        """Add and configure a new channel"""
        self._channels[name] = AsyncConsumerPublisherChannel(self._connection, await self._connection.channel())
        await configure_channel(self._channels[name])
        return self._channels[name]

    def get_channel(self, name):
        return self._channels[name]

    async def consume_all(self, channel_name):
        """Start consuming on all specific registered consumer of a channel on a single task"""
        await self._channels[channel_name].consume_all()

    async def close(self):
        for _, channel in self._channels.items():
            await channel.close()
        await self._connection.close()
