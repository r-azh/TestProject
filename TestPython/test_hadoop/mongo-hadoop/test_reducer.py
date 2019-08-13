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
    # _count = 0
    dict = {'_id': key}
    for v in values:
        dict.update(v)
        # _count += v['count']
    #         _sum += v['bc10Year']
    # return {'_id': key, 'avg': _sum / _count,
    #         'count': _count, 'sum': _sum }
    #print({'_id': key, 'count': _count})
    # return {'_id': key, 'count': _count}
    return dict

BSONReducer(reducer)