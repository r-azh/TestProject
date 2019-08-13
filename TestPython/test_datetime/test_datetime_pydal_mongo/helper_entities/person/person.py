from bson import ObjectId

__author__ = 'R.Azh'


class Person:
    _id = None
    name = None
    last_Name = None
    birthday = None

    def __init__(self, dict):
        self.__dict__.update(dict)
        # self._id = ObjectId()

