import os
import asyncio
import json
import logging
from ..drivers import AMQPClient, GraphDriver, MongoDriver, IndexDriver
from ..datastore import Datastore
from ..tasks import TaskConsumer


async def create_amqp_client(loop):
    """ Create an amqp client ready for connection """
    amqp_url = f"amqp://{os.environ['RABBITMQ_USER']}:{os.environ['RABBITMQ_PWD']}@{os.environ['RABBITMQ_HOST']}:{os.environ['RABBITMQ_PORT']}"
    exchange_name = f"{os.environ['ENV']}-{os.environ['SOLUTION_NAME']}"
    amqp_client = AMQPClient(amqp_url, exchange_name, loop)
    return amqp_client


async def create_datastore(
    loop,
    amqp_client,
    json_schema,
    nodes_namespace_uri,
    nodes_prefix,
    namespace_mapping,
    model_class_mapping=None,
    use_rdf=True,
    use_index=True,
    use_mongo=True
):
    """ Helper for creating a datastore with drivers and schema """

    graph_driver = index_driver = mongo_driver = None

    # Instanciate driver for querying graph triplestore
    if use_rdf:
        graph_driver = GraphDriver(
            amqp_client,
            f"{os.environ['MODULE_ID']}-graph-driver",
            os.environ['RDF_REPOSITORY_NAME'],
            namespace_mapping,
            nodes_namespace_uri,
            nodes_prefix
        )

    # Instanciate driver for querying index
    if use_index:
        index_driver = IndexDriver(
            host=os.environ['ES_HOST'],
            port=os.environ['ES_PORT'],
            user=os.environ['ES_USER'],
            pwd=os.environ['ES_PWD'],
            index_prefix=os.environ['INDEX_PREFIX']
        )

    # Instanciate driver for querying mongo
    if use_mongo:
        mongo_url = f"mongodb://{os.environ['MONGO_USER']}:{os.environ['MONGO_PWD']}@{os.environ['MONGO_ENDPOINT']}"
        mongo_driver = MongoDriver(mongo_url, os.environ['MONGO_DATABASE'])

    # Define datastore with model layer and database drivers
    datastore = Datastore(
        json_schema,
        namespace_mapping,
        nodes_namespace_uri,
        nodes_prefix,
        graph_driver,
        mongo_driver,
        index_driver,
        # mapper for model classes, necessary for using model layer
        model_class_mapper=model_class_mapping
    )

    return datastore
