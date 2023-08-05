from .keys import DATATYPE_MAPPER, KEY_NAME, KEY_RDF_TYPE, KEY_INDEX_TYPE,\
    KEY_MONGO_TYPE, KEY_DATATYPE, KEY_RELATED_TYPE, KEY_NESTED, KEY_PLURAL, \
    KEY_INTERNAL_PROP


class Model(object):
    """ Model base class for all objects queried from graph """

    _internal_props: object
    _schema: object
    _datastore: object

    def __init__(self, props, schema, datastore):
        self._internal_props = props
        self._schema = schema
        self._datastore = datastore

    @classmethod
    async def load(cls, object_id, datastore):
        """ Query an object through datastore and instanciate corresponding model """
        schema_type = cls.get_schema_type()
        graph_object = await datastore.get_object(schema_type, object_id)
        if not graph_object:
            return None
        return datastore.to_model(schema_type, graph_object)

    @property
    def id(self):
        return self.get_prop('id')

    def get_prop(self, name):
        """ Get prop from internal props if existing else None """
        prop_spec = self._schema.get("props", {}).get(name, None)
        if not prop_spec:
            raise Exception(f'Property {name} not in schema : ${self._schema}')

        target_datatype = prop_spec[KEY_DATATYPE]
        is_plural = prop_spec[KEY_PLURAL]
        if target_datatype not in DATATYPE_MAPPER:
            raise Exception(f'Datatype {target_datatype} not in datatype mapper')

        convert_to_type = DATATYPE_MAPPER[target_datatype]
        prop_value = self._internal_props.get(name, None)
        if not prop_value:
            return [] if is_plural else None

        if not is_plural:
            value = prop_value[0] if isinstance(prop_value, list) else prop_value
            return convert_to_type(value)

        return [convert_to_type(v) for v in prop_value]

    async def get_link(self, name):
        """ Get prop from internal props if existing, and query datastore for getting matching objects with ids """
        links = self._schema.get("links", {})
        link_spec = links.get(name, None)
        if not link_spec:
            link_spec = next((spec for spec in links.values() if spec[KEY_INTERNAL_PROP] == name), None)
        if not link_spec:
            raise Exception(f'Property {name} not in schema : ${self._schema}')

        related_type = link_spec[KEY_RELATED_TYPE]
        is_plural = link_spec[KEY_PLURAL]
        is_nested = link_spec[KEY_NESTED]

        targets = self._internal_props.get(name, None)
        if not targets or len(targets) == 0:
            return [] if is_plural else None

        targets = [targets] if not isinstance(targets, list) else targets

        if not is_nested:
            targets = await self._datastore.get_objects(related_type, targets)

        targets = [self._datastore.to_model(related_type, target) for target in targets]
        return targets if is_plural else targets[0] if len(targets) > 0 else None

    def to_json(self):
        """ Return model object as json """
        return {**self._internal_props}
