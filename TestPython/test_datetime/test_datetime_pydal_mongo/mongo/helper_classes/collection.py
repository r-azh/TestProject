from TestPython.test_datetime.test_datetime_pydal_mongo.mongo.helper_classes.read import ReadCommand
from TestPython.test_datetime.test_datetime_pydal_mongo.mongo.helper_classes.write import WriteCommand

__author__ = 'Hooman'


class Collection:
    def __init__(self, collection_name, mongo_collection):
        self.collection_name = collection_name
        self._mongo_collection = mongo_collection

    def create_index(self, indexes_dict):
        indexes = [(k, v) for k, v in indexes_dict.items()]
        self._mongo_collection.create_index(indexes)

    def _get_reader(self):
        pydal_reader = ReadCommand(self._mongo_collection)
        return pydal_reader

    def _get_writer(self):
        pydal_writer = WriteCommand(self._mongo_collection)
        return pydal_writer

    reader = property(_get_reader)
    writer = property(_get_writer)
