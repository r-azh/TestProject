from pymongo import MongoClient

mongo_con = MongoClient('localhost', 27017)
db = mongo_con['test']
coll = db['test']

document = {'name': 'test', 'family': 'testf', 'age': 2}
coll.insert(document)

res = coll.find_and_modify(
    {
        '$query': {'name': 'test'},
        '$sort': {'name': 1},
        '$remove': True})

# res = coll.find_one_and_delete({'name': 'test'})
# res = coll.find_and_delete({'name': 'test'})
print(res)
