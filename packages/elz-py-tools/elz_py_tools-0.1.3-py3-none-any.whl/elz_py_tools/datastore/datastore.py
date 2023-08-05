import json
from ..drivers import GraphDriver, MongoDriver, IndexDriver
from .model import Model
from .keys import DATATYPE_MAPPER, KEY_NAME, KEY_RDF_TYPE, KEY_INDEX_TYPE,\
    KEY_MONGO_TYPE, KEY_DATATYPE, KEY_RELATED_TYPE, KEY_NESTED, KEY_PLURAL


class Datastore(object):
    """ Datastore for uniformizing query to graph and mongo databases """

    _schema_types: object
    _prefixes_mapping: object
    _nodes_namespace_uri: str
    _nodes_prefix: str
    _graph_driver: GraphDriver
    _mongo_driver: MongoDriver
    _index_driver: IndexDriver
    _model_class_mapper: object

    def __init__(
        self,
        json_schema: str,
        prefixes_mapping: object,
        nodes_namespace_uri: str,
        nodes_prefix: str,
        graph_driver: GraphDriver = None,
        mongo_driver: MongoDriver = None,
        index_driver: IndexDriver = None,
        model_class_mapper: object = None,
    ):
        self._schema_types = json_schema
        self._prefixes_mapping = prefixes_mapping
        self._nodes_namespace_uri = nodes_namespace_uri
        self._nodes_prefix = nodes_prefix
        self._graph_driver = graph_driver
        self._mongo_driver = mongo_driver
        self._index_driver = index_driver
        self._model_class_mapper = model_class_mapper

    def get_mongo_driver(self):
        return self._mongo_driver

    def get_graph_driver(self):
        return self._graph_driver

    def get_index_driver(self):
        return self._index_driver

    def close_connections(self):
        """ Close driver connections """
        self._mongo_driver.close()

    def get_schema_type(self, typename: str):
        """ Return schema corresponding to typename """
        return next((schema for schema in self._schema_types.values() if schema[KEY_NAME] == typename), None)

    async def get_objects(self, typename: str, object_ids: [str] = None, use_graph: bool = False):
        """ Return all objects of type defined in argument
            Results are merged objects of triplestore and mongo databases
        """
        schema_spec = self.get_schema_type(typename)
        if not schema_spec:
            raise Exception(f'Unknow type {typename}')

        graph_type = schema_spec.get(KEY_RDF_TYPE, None)
        index_type = schema_spec.get(KEY_INDEX_TYPE, None)
        mongo_type = schema_spec.get(KEY_MONGO_TYPE, None)

        graph_objects = []
        mongo_objects = []

        if not use_graph and self._index_driver and index_type:
            document_ids = list(map(lambda x: self.to_absolute_uri(x), object_ids)) if object_ids else None
            graph_objects = await self._index_driver.get_nodes(index_type, document_ids)
            graph_objects = [{**obj, "id": self.to_prefixed_uri(obj["id"])} for obj in graph_objects]
        elif self._graph_driver and graph_type:
            if object_ids:
                raise Exception('Query GraphIndex.getNodes with objects_ids is not yet supported...')
            graph_objects = await self._graph_driver.get_nodes(graph_type)
            graph_objects = [{**obj, "id": self.to_prefixed_uri(obj["id"])} for obj in graph_objects]

        if self._mongo_driver and mongo_type:
            mongo_ids = list(map(lambda x: self.to_prefixed_uri(x), object_ids)) if object_ids else None
            mongo_objects = self._mongo_driver.find_documents(mongo_type, mongo_ids)

        merged_objects = []
        mongo_objects_id = list(map(lambda x: x['id'], mongo_objects))
        if graph_type:
            for graph_object in graph_objects:
                matching_mongo_object = next((obj for obj in mongo_objects if obj['id'] == graph_object['id']), None) or {}
                merged_objects.append({
                    **graph_object,
                    **matching_mongo_object,
                    "type": typename
                })
        else:
            merged_objects = mongo_objects

        return merged_objects

    async def get_object(self, typename: str, object_id: str, use_graph=False):
        """ Return object corresponding to id and type defined in argument
            Result is merge of object found in triplestore and mongo databases if any
        """
        schema_spec = self.get_schema_type(typename)
        if not schema_spec:
            raise Exception(f'Unknow type {typename}')

        graph_type = schema_spec.get(KEY_RDF_TYPE, None)
        index_type = schema_spec.get(KEY_INDEX_TYPE, None)
        mongo_type = schema_spec.get(KEY_MONGO_TYPE, None)

        graph_object = {}
        mongo_object = {}

        if not use_graph and self._index_driver and index_type:
            graph_object = await self._index_driver.get_node(index_type, self.to_absolute_uri(object_id))
            graph_object = {**graph_object, "id": self.to_prefixed_uri(graph_object['id'])} if graph_object else None
        elif self._graph_driver and graph_type:
            graph_object = await self._graph_driver.get_node(graph_type, self.to_absolute_uri(object_id))
            graph_object = {**graph_object, "id": self.to_prefixed_uri(graph_object['id'])} if graph_object else None

        if self._mongo_driver and mongo_type:
            mongo_object = self._mongo_driver.find_document(mongo_type, self.to_prefixed_uri(object_id)) or None

        if not graph_object and not mongo_object:
            return None

        merged_object = {
            **(graph_object or {}),
            **(mongo_object or {}),
            "type": typename
        }

        return merged_object

    def to_absolute_uri(self, uri: str):
        """ Convert an uri into absolute uri """
        if uri.startswith('http://'):
            return uri
        elif self._nodes_prefix in uri:
            return uri.replace(f'{self._nodes_prefix}:', f'{self._nodes_namespace_uri}/')
        else:
            matching_prefix = next((prefix for prefix in self._prefixes_mapping.keys() if prefix in uri), None)
            if matching_prefix:
                return uri.replace(f'{matching_prefix}:', self._prefixes_mapping[matching_prefix])
        # Last case: no prefix at all, we put nodes namespace uri
        return f'{self._nodes_namespace_uri}/{uri}'

    def to_prefixed_uri(self, uri: str):
        """ Convert an uri into prefixed uri """
        if f'{self._nodes_prefix}:' in uri:
            return uri
        elif ':' not in uri and '#' not in uri:
            return f'{self._nodes_prefix}:{uri}'
        elif self._nodes_namespace_uri in uri:
            return uri.replace(f'{self._nodes_namespace_uri}/', f'{self._nodes_prefix}:')
        else:
            prefix, ns_uri = next(
                ((prefix, ns_uri) for prefix, ns_uri in self._prefixes_mapping.items() if ns_uri in uri), (None, None)
            )
            if ns_uri:
                if '#' in uri:
                    return uri.replace(f'{ns_uri}#', f'{prefix}:')
                else:
                    return uri.replace(f'{ns_uri}/', f'{prefix}:')

        # Last case: no prefix at all, we put nodes prefix
        return f'{self._nodes_prefix}:{uri}'

    def to_id(self, uri: str):
        """ Convert an uri into id """
        uri = uri.replace(f'{self._nodes_namespace_uri}/', '')
        uri = uri.replace(f'{self._nodes_prefix}:', '')
        return uri

    def to_model(self, typename, obj):
        """ Instanciate object as a class matching typename in argument
            Raise exception if model_class_mapper was not defined in datastore
            Raise as well exception if model class not found
        """
        if not self._model_class_mapper:
            raise Exception("Cannot call 'Datastore.to_model' function as no class mapper was passed to Datastore")

        schema_type = self.get_schema_type(typename)
        model_cls = self._model_class_mapper.get(typename, Model)
        if not model_cls:
            raise Exception(f"No model class defined for object of type {typename}")

        return model_cls(obj, schema_type, self)
