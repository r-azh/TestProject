from bson import ObjectId
from pymongo import MongoClient, bulk

__author__ = 'R.Azh'


mongo_con = MongoClient('localhost', 27017)
db = mongo_con['test']
coll = db.test


document = {'name': 'test', 'family': 'testf', 'age': 2}
# coll.insert(document)

# coll.update({'name': 'test'}, {'family': 'uuppddaatteedd', 'age': 3}, upsert=True) # not true when there is no doc

document2 = {'name': 'test', 'family': 'testf2', 'age': 4}
# coll.update({'name': 'test'}, document2, upsert=True)   #dorost
#
# coll.update({'name': 'test'}, document, upsert=True)

doc_list = []
# doc = {} # adds just one element to doc_list
for i in range(1, 20):
    doc = {}
    doc['name'] = 'name_' + str(i)
    doc['family'] = '*family_' + str(i)
    doc['age'] = i
    doc_list.append(doc)
print(doc_list)

bulk_op = coll.initialize_ordered_bulk_op()
for doc in doc_list:
    bulk_op.find({'name': doc['name']}).upsert().update_one({'$set': {'family': doc['family']}})
    print(doc)
bulk_op.execute()

print(ObjectId())