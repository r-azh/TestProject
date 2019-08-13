__author__ = 'R.Azh'

import pymongo
mongo = "mongodb://user:pass@localhost:27017/admin"

mc = pymongo.MongoClient(mongo)
colleciton = pymongo.MongoClient(mongo)['users_list']['users']


import pprint
pprint.pprint(mc.server_info())


x = colleciton.find()
print(x[1])

ag = colleciton.aggregate([
    {'$group': {
        '_id': '$full_name',
        'count': {'$sum': 1}
    }}], useCursor=False)
print(list(ag))
