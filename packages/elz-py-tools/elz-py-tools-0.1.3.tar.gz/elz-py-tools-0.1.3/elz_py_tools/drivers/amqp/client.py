import uuid
import json
import logging
import traceback
from typing import Callable
from functools import partial
from aio_pika import connect_robust, IncomingMessage, Message, Exchange, ExchangeType


LOGGER = logging.getLogger(__name__)


class AMQPClient(object):
    """AMQP client for connecting a rabbitMQ bus"""

    def __init__(self, amqp_url: str, exchange_name: str, loop, options={}):
        self._url = amqp_url
        self._exchange_name = exchange_name
        self._loop = loop
        self._prefetch_count = options.get('prefetch_count', 10)
        self._connection = None
        self._channel = None
        self._futures = {}
        self._consumer_id = str(uuid.uuid4())
        self._listening_queue_number = 0

        self._rpc_callback_queue = None

    async def connect(self):
        """ Connect to the amqp bus """
        self._connection = await connect_robust(self._url, loop=self._loop)
        self._channel = await self._connection.channel()
        await self._channel.set_qos(prefetch_count=1)

        await self._channel.declare_exchange(self._exchange_name, ExchangeType.TOPIC)

        rpc_queue_name = f"{self._exchange_name}_{self._consumer_id}_rpc_callback_queue"
        self._rpc_callback_queue = await self._channel.declare_queue(rpc_queue_name,
                                                                     exclusive=True,
                                                                     auto_delete=True,
                                                                     durable=False)

        await self._rpc_callback_queue.consume(self._on_rpc_response, no_ack=True)

        return self

    async def publish(self, command: str, body: object, options={}):
        """ Publish a message to the bus """
        if self._channel is None:
            raise Exception('AMQP client is not connected')

        exchange = await self._channel.get_exchange(self._exchange_name)  \
            if self._exchange_name \
            else self._channel.default_exchange

        await exchange.publish(
            Message(
                json.dumps(body).encode(),
                content_type=options.get("content_type", "application/json"),
                correlation_id=options.get("correlation_id", None),
                reply_to=options.get("reply_to", None)
            ),
            routing_key=command,
            mandatory=options.get("mandatory", True)
        )

    async def request(self, command: str, body: object):
        """ Trigger a RPC call with command value as routing_key, and wait for result before return """
        correlation_id = str(uuid.uuid4())
        future = self._loop.create_future()

        self._futures[correlation_id] = future

        await self.publish(command, body, {
            "content_type": "application/json",
            "correlation_id": correlation_id,
            "reply_to": self._rpc_callback_queue.name
        })

        return await future

    async def listen(self, routing_key: str, callback: Callable[[object], object], queue_name=None):
        """ Listen for messages passing on queue_name with routing_key, and executes callback
            if queue_name is not defined, a custom and unique queue_name is used
        """
        if self._channel is None:
            raise Exception('AMQP client is not connected')

        routing_key = routing_key or '#'
        self._listening_queue_number = self._listening_queue_number + 1
        queue_name = queue_name or f"{self._exchange_name}_{self._consumer_id}_{self._listening_queue_number}:{routing_key}"

        queue = await self._channel.declare_queue(queue_name, exclusive=True, auto_delete=True, durable=False)

        listen_exchange = await self._channel.get_exchange(self._exchange_name)  \
            if self._exchange_name \
            else self._channel.default_exchange
        await queue.bind(listen_exchange, routing_key=routing_key)

        await queue.consume(partial(self._on_listen_callback, self._channel.default_exchange, callback))

    def _on_rpc_response(self, message: IncomingMessage):
        """ RPC response
            Future linked to RPC call got message result, and so we can keep running code with response
        """
        try:
            future = self._futures.pop(message.correlation_id)
            future.set_result(message.body.decode())
        except Exception as e:
            print(message)

    async def _on_listen_callback(self, exchange: Exchange, callback: Callable[[object], object], message: IncomingMessage):
        """ Listen response wrapper
            This wrapper process message through callback, and send back response if reply_to is defined in message
        """
        with message.process():
            body = json.loads(message.body.decode())
            try:
                result = await callback(body)
                response = {
                    "headers": {"status": "OK "},
                    "body": result
                }
            except Exception as e:
                LOGGER.error(f'Error "{str(e)}" occurred on message : {message}')
                LOGGER.error(traceback.format_exc())
                response = {
                    "headers": {"status": "ERROR"},
                    "body": {"errorMessage": f'An error occurred on processing message, see logs...'}
                }

            if message.reply_to:
                await exchange.publish(
                    Message(
                        content_type="application/json",
                        body=json.dumps(response).encode(),
                        correlation_id=message.correlation_id
                    ),
                    routing_key=message.reply_to,
                )
