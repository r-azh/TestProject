from TestPython.test_datetime.test_datetime_pydal_mongo.mongo.helper_classes.connection import Connection

__author__ = 'H.Rouhani'


class Repository:
    def __init__(self, collection):
        connection = Connection("mongodb://localhost:27017")
        self.collection = connection.db("test_db").collection(collection)

    def create(self, item):
        self.collection.writer.add(item)

    def delete(self, id):
        self.collection.writer.remove_by_id(id)

    def update(self, item):
        self.collection.writer.edit(item)
