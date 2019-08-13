from pymongo.mongo_client import MongoClient
from TestPython.test_datetime.test_datetime_pydal_mongo.mongo.helper_classes.db import Db

__author__ = 'Hooman'


class Connection:
    def __init__(self, connection_string):
        self._connection_string = connection_string
        self._mongo_connection = MongoClient(connection_string)

    def db(self, name):
        mongodb = self._mongo_connection[name]
        db = Db(name, mongodb)
        return db


