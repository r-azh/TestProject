__author__ = 'R.Azh'

import pymongo
client = pymongo.MongoClient('localhost', 27017)
db = client.testdatabase
col = db.testcollection
col.insert({'FixedH': False,'Mstereo': True,'RecMet': False,'Sstereo': True,'bond': False,
            'charge': False, 'isotope': False,'length': 223,'nocomponents': 1,
            'nolayers': 6,'stereo': True})
cursor = col.find()
print('Found', cursor.count())
print(cursor.next())
client.close()

cursor = col.find({'FixedH': False})
for document in cursor:
    print(document)

###########################
import jsonpickle

d = jsonpickle.dumps(True)
print(d)
print(type(d))

import json
o = json.loads(d)
print(o)
print(type(o))

d2 = json.dumps(True)
print(d2)
print(type(d2))

print(True and not (5 == 4))


print('######################\n')
is_a = False
is_b = True
is_c = None

print(is_a or False)
print(is_a or True)
print(is_b or False)
print(is_b or True)
print(is_c or False)
print(is_c or True)

print('######################\n')
print("Hallo" if True else "Tchus")
print("Hallo" if False else "Tchus")

dict = {}
print('True' if {} else "False")
