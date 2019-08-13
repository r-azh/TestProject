__author__ = 'R.Azh'


def get_methods(object):
    methodList = [method for method in dir(object) if callable(getattr(object, method))]
    return methodList


import pymongo
methods = get_methods(pymongo)
print(methods)