from datetime import datetime

from bson import ObjectId

from TestPython.test_datetime.test_datetime_pydal_mongo.helper_entities.person.person import Person
from TestPython.test_datetime.test_datetime_pydal_mongo.helper_entities.person.person_mongo_read import PersonMongoRead
from TestPython.test_datetime.test_datetime_pydal_mongo.helper_entities.person.person_mongo_write import PersonMongoWrite

__author__ = 'R.Azh'

person_dict = {"name": "bill", "last_name": "gates", "birthday": datetime(2008, 12, 4, 12, 30), "_id": str(ObjectId())}
test_person = Person(person_dict)
print(test_person.__dict__)

PersonMongoWrite().create(test_person)

read_test_person = PersonMongoRead().get_by_id(test_person._id)
print(read_test_person)



