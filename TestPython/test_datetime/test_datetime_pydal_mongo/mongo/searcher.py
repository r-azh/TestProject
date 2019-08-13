from bson import ObjectId
from TestPython.test_datetime.test_datetime_pydal_mongo.mongo.helper_classes.connection import Connection

__author__ = 'H.Rouhani'


class Searcher:
    def __init__(self, collection):
        connection = Connection("mongodb://localhost:27017")
        self.collection = connection.db("test_db").collection(collection)

    def get_by_id(self, id):
        return self.collection.reader.find_one({"_id": ObjectId(id)})

    def exist_id(self, id):
        return self.collection.reader.is_available({"_id": ObjectId(id)})
