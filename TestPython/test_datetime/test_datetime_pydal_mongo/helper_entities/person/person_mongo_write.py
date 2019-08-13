from TestPython.test_datetime.test_datetime_pydal_mongo.mongo.repository import Repository

__author__ = 'R.Azh'


class PersonMongoWrite(Repository):
    def __init__(self):
        super(PersonMongoWrite, self).__init__("person")