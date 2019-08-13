from datetime import datetime
from bson import ObjectId
from TestPython.test_datetime.test_datetime_pydal_mongo.serializer.json.handler import DatetimeHandler, \
    ObjectIdBsonSerializeHandler
from TestPython.test_datetime.test_datetime_pydal_mongo.serializer.json.serializer import Serializer


class WriteCommand:
    def __init__(self, mongo_collection):
        self._mongo_collection = mongo_collection

    def save(self, data):
        serialized_data_dictionary = self._get_document(data)
        self._mongo_collection.save(serialized_data_dictionary)

    def add(self, data):
        serialized_data_dictionary = self._get_document(data)
        self._mongo_collection.insert(serialized_data_dictionary)

    def edit(self, data):
        serialized_data_dictionary = self._get_document(data)
        self._mongo_collection.update({"_id": serialized_data_dictionary["_id"]}, serialized_data_dictionary)

    def edit_by_condition(self, first_query, second_query, multi=True):
        self._mongo_collection.update(first_query, second_query, multi=multi)

    def remove_by_id(self, id_string):
        self._mongo_collection.remove({"_id": ObjectId(id_string)})

    def remove_by_condition(self, query):
        self._mongo_collection.remove(query)

    def remove_all(self):
        self._mongo_collection.remove({})

    def _get_document(self, data):
        if not hasattr(data, "_id") or not data._id:
            data._id = ObjectId()
        elif isinstance(data._id, str):
            data._id = ObjectId(data._id)
        json_serializer = Serializer()
        json_serializer.add_handler(datetime, DatetimeHandler)
        # json_serializer.add_handler(ObjectId, ObjectIdBsonSerializeHandler)
        document = json_serializer.serialize_to_dictionary(data)
        data._id = str(data._id)
        return document