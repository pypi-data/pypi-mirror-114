import logging
from aio_pika import IncomingMessage
from ..drivers import AMQPClient


LOGGER = logging.getLogger(__name__)


class TaskConsumer(object):
    """Wrapper for listening amqp bus and triggering tasks"""

    _amqp_consumer: AMQPClient

    def __init__(self, amqp_client: AMQPClient, routing_keys: [str]):
        self._amqp_consumer = amqp_client
        self._routing_keys = routing_keys
        self._callbacks = {}

    def bind(self, command: str, callback):
        """Bind a callback to command"""
        if command not in self._callbacks:
            self._callbacks[command] = []
        self._callbacks[command].append(callback)

    async def listen(self):
        """Listen on bus, for routing keys defined in contructor"""
        for routing_key in self._routing_keys:
            await self._amqp_consumer.listen(routing_key, self._on_message)

    async def _on_message(self, message: IncomingMessage):
        """Dispatch message to the matching callback"""
        command = message["headers"]["command"]
        if command not in self._callbacks:
            raise Exception(f'Task consumer received unhandled message of type {command}')

        for callback in self._callbacks[command]:
            try:
                response = await callback(message["body"])
            except Exception as e:
                # TODO: send mail to a support address ?
                raise e

        return response
