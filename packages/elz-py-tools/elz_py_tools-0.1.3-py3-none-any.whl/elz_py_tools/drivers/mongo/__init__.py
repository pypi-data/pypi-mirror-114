from typing import TypedDict
from pymongo import MongoClient


class MongoDriver(object):
    """ Driver for mongo database """

    def __init__(self, url, db_name):
        self._db_name = db_name
        self._mongo_client = mongo_client = MongoClient(url)[self._db_name]

    def close(self):
        """ Close mongo connection """
        self._mongo_client.close()

    def get_collection_names(self):
        """ Return names of existing collections in mongo database """
        return self._mongo_client.list_collection_names()

    def find_document(self, collection_name: str, object_id: str, filters: [{'prop': str, 'value': str}] = {}):
        """ Find document with id in parameter, from collection type defined, and using filters if any """
        if type(object_id) is not str:
            raise Exception(f'mongo.find_document : "object_id" must be a string')
        collection = self._mongo_client[collection_name]
        if collection is None:
            raise Exception(f'Mongo error : {collection_name} is not existing in {self._db_name}')

        filters = {**filters, "_id": object_id}

        found_object = list(collection.find(filters))
        if not found_object or len(found_object) == 0:
            return None

        return self._parse_result(list(found_object))[0]

    def find_documents(self, collection_name: str, object_ids: [str] = None, filters: [{'prop': str, 'value': str}] = {}):
        """ Find documents with ids in parameter, and using filters if any
            If no ids are provided, returns all documents for collection type in parameter
        """
        if object_ids and type(object_ids) is not list:
            raise Exception(f'mongo.find_document: "object_ids" must be a list')
        collection = self._mongo_client[collection_name]
        if collection is None:
            raise Exception(f'Mongo error : {collection_name} is not existing in {self._db_name}')

        if object_ids:
            filters = {**filters, "_id": {"$in": object_ids}}

        found_objects = list(collection.find(filters))
        return self._parse_result(found_objects)

    def _parse_result(self, objects: [object]):
        """ Pop _id and __v properties from result, and populate an id field """
        parsed_objects = []
        for obj in objects:
            parsed_object = {**obj, 'id': obj['_id']}
            parsed_object.pop('_id')
            parsed_object.pop('__v', None)
            parsed_objects.append(parsed_object)
        return parsed_objects
