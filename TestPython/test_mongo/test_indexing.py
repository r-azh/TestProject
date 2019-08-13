from pprint import pprint
import pymongo


__author__ = 'R.Azh'

mongo_con = pymongo.MongoClient('localhost', 27017)
db = mongo_con['test_db']

db.test_collection.drop_indexes()
db['test_collection'].drop_indexes()
pprint(db['test_collection'].find().explain())

# single key index
result = db['test_collection'].create_index([('parent_post_id', pymongo.ASCENDING)])
# All optional index creation parameters should be passed as keyword arguments to this method
# http://api.mongodb.com/python/current/api/pymongo/collection.html

# compound  index (order is important)
result = db.test_collection.create_index([('parent_post_id', pymongo.ASCENDING), ('parent_first_level_comment_id',
                                                                                  pymongo.ASCENDING),
                                          ('container_id', pymongo.DESCENDING), ('creator.person_id', 1)])
print(result)

print('indexes: ', db['test_collection'].list_indexes())
print('indexes: ', db['test_collection'].index_information())

db.test_collection.drop_index([('parent_post_id', pymongo.ASCENDING)])

# create multiple index at once
index1 = pymongo.IndexModel([("hello", -1),
                             ("world", 1)], name="hello_world")
index2 = pymongo.IndexModel([("goodbye", -1)])
db.test_collection.create_indexes([index1, index2])

db.test_collection.drop_index("hello_world")

print('indexes: ', db['test_collection'].index_information())


pprint(db['test_collection'].find().explain()['executionStats'])

# for not creating index multiple times
index_name = 'Datetime'
if index_name not in db.test_collection.index_information():
    db.test_collection.create_index(index_name, unique=True)

index_dict = {'parent_post_id': 1, 'parent_first_level_comment_id': 1,
              'container_id': 1, 'creator.person_id': 1}
index_info = db.test_collection.index_information()
# mongo_index =
print(index_info)
