from bson import ObjectId

__author__ = 'R.Azh'

from pydal.mongo.connection import Connection

pydalConnection = Connection("mongodb://localhost:27017")
pydalCollection = pydalConnection \
    .db("pydalDb") \
    .collection("Developer")


class Sample:
    _id = None
    field_1 = None
    field_2 = None

    def __init__(self):
        self._id = ObjectId()
        self.field_1 = True
        self.field_2 = False


obj = Sample()

pydalCollection.writer.add(obj)
read_obj = pydalCollection.reader.find_one({"_id": ObjectId(obj._id)})
print(read_obj.__dict__)

pydalCollection.writer.edit_by_condition({"_id": ObjectId(obj._id)},
                                                 {"$set": {"field_1": False}})

read_obj = pydalCollection.reader.find_one({"_id": ObjectId(obj._id)})
print(read_obj.__dict__)


read_obj = pydalCollection.reader.find_one({"field_2": False})
print(read_obj.__dict__)


read_objs = pydalCollection.reader.find_many(fields=[], query={"field_2": False}, skip=0, take=150)
for obj in read_objs:
    print(obj.__dict__)


read_objs2 = pydalCollection.reader.find_many({})
print(read_objs2)

# read_obj = pydalCollection.reader.aggregate(fields=[], query={"field_2": False})
# print(read_obj)