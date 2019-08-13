from datetime import datetime
from bson import ObjectId
from TestPython.test_datetime.test_datetime_pydal_mongo.helper_entities.person.person import Person

__author__ = 'R.Azh'

person_dict = {"name": "bill", "last_name": "gates", "birthday": datetime(2008, 12, 4, 12, 30), "_id": str(ObjectId())}
test_person = Person(person_dict)
print(test_person.__dict__)

import pymongo
client = pymongo.MongoClient('localhost', 27017)
db = client.test_db
collecion = db.test_date_collection

# collecion.insert(test_person)  # gives: 'Person' object is not iterable
collecion.insert(person_dict)
read_test_person = collecion.find({"_id": test_person._id})
print(read_test_person.next())

