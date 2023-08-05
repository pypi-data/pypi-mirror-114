import json
import os
import datetime
from .publisher import GraphPublisher
from .parser import parse_construct_result
from .sparql import SPARQLBuilder


class GraphDriver(object):
    """ Driver for triplestore database """

    def __init__(self, amqp_client, sender_id, repository_name, prefixes_mapping, nodes_namespace_uri, nodes_prefix):
        self._publisher = GraphPublisher(amqp_client, sender_id, repository_name)
        self._sparql_builder = SPARQLBuilder(prefixes_mapping, nodes_namespace_uri, nodes_prefix)

    def get_graph_publisher(self):
        return self._publisher

    async def raw_select(self, query: str):
        """ Executes a raw select query
            Is equivalent to get publisher from this object and call its select method
        """
        result = await self._publisher.select(query)
        return result

    async def raw_construct(self, query: str, parse_result=True):
        """ Executes a raw construct query
            if parse_result is True, parse bindings result and convert into properties grouped by entity returned
        """
        bindings = await self._publisher.construct(query)
        if parse_result:
            objects = parse_construct_result(bindings)
        else:
            objects = bindings
        return objects

    async def get_nodes(self, node_type: str, object_ids: [str] = None):
        """ Get nodes and their properties corresponding to node_type """
        sparql_query = self._sparql_builder.build_construct_objects_query(node_type)
        bindings = await self._publisher.construct(sparql_query)
        objects = parse_construct_result(bindings)
        return objects

    async def get_node(self, node_type: str, object_id: str):
        """ Get node and its properties for node_type and object_id """
        sparql_query = self._sparql_builder.build_construct_object_query(node_type, object_id)
        bindings = await self._publisher.construct(sparql_query)
        objects = parse_construct_result(bindings)
        return objects[0] if len(objects) > 0 else None
