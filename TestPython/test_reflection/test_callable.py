__author__ = 'R.Azh'
# the callable function takes any object and returns True if the object can be called,
#  or False otherwise. Callable objects include functions, class methods, even classes themselves.

import string

print(string.punctuation)
print(callable(string.punctuation))

import pymongo
print(callable(pymongo.ReplaceOne))
print(pymongo.ReplaceOne.__doc__)