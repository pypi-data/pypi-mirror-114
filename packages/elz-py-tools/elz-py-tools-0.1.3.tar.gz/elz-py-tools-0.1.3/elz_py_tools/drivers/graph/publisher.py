import uuid
import datetime
import logging
import json
from ..toolkit.publisher import AbstractPublisher
from .. import AMQPClient


class GraphPublisher(AbstractPublisher):
    """ Extends publisher to serve methods adapted to graph queries """

    def __init__(self, amqp_driver: AMQPClient, sender_id: str, repository_name: str):
        super(GraphPublisher, self).__init__(amqp_driver, sender_id)
        self._repository_name = repository_name

    async def ask(self, query: str):
        """ Executes ASK query in parameter """
        if 'ASK' not in query:
            raise Exception(f'Use ask select method for doing a select query')
        return await self.publish('graph.ask', query, {
            "format": "SPARQL",
            "repositories": [self._repository_name]
        })

    async def select(self, query: str):
        """ Executes SELECT query in parameter """
        if 'SELECT' not in query:
            raise Exception(f'Use publisher construct method for doing a construct query')
        return await self.publish('graph.select', query, {
            "format": "SPARQL",
            "repositories": [self._repository_name]
        })

    async def construct(self, query: str):
        """ Executes CONSTRUCT query in parameter """
        if 'CONSTRUCT' not in query:
            raise Exception(f'Use publisher select method for doing a select query')
        return await self.publish('graph.construct', query, {
            "format": "SPARQL",
            "repositories": [self._repository_name]
        })
