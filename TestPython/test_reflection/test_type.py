__author__ = 'R.Azh'

print(type(1))
li = []
print(type(li))
tu = ("1", "a", 30)
print(type(tu))

import pymongo
print(type(pymongo))

import types
print(type(types.FunctionType))

print(type(None))

if isinstance(tu, tuple):
    print('tuple')
    if len(tu) == 3:
        print('right')


