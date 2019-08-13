from TestPython.test_datetime.test_datetime_pydal_mongo.mongo.helper_classes.collection import Collection

__author__ = 'Hooman'


class Db:
    def __init__(self, db_name, mongodb):
        self.db_name = db_name
        self.mongodb = mongodb

    def collection(self, name):
        mongo_collection = self.mongodb[name]
        pydal_collection = Collection(name, mongo_collection)
        return pydal_collection

