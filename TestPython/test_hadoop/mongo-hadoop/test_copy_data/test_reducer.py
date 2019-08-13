__author__ = 'R.Azh'

# !/usr/bin/env python  # for centos
# !/usr/bin/python  # for ubuntu

# pip3 install pyarrow, pandas
# copy pymongo-hadoop from the source to dist-packages

import sys
sys.path.append(".")

from pymongo_hadoop import BSONReducer


def reducer(key, values):
    print(sys.stderr, "Processing data %s" % key)
    dict = {'_id': key}
    for v in values:
        dict.update(v)
    return dict

BSONReducer(reducer)
