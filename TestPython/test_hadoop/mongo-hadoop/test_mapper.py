__author__ = 'R.Azh'
#!/usr/bin/env python  # for centos
#!/usr/bin/python  # for ubuntu

# pip3 install pyarrow, pandas
# copy pymongo-hadoop from the source to dist-packages

import bson

bson.BSON

import sys
sys.path.append(".")

from pymongo_hadoop import BSONMapper


def mapper(documents):
    for doc in documents:
        # IMPORTANT : THIS PRINT WONT LET REDUCE TO PUT RESULT IN MONGO BECAUSE PRINT USES STANDARDAD OUTPUT TOO
        # print({'_id': doc['_id'].year, 'count': 1})
        #yield {'_id': doc['_id'].year, 'count': 1}
        yield doc
        #        yield {'_id': doc['_id'].year, 'bc10Year': doc['bc10Year']}


BSONMapper(mapper)
print(sys.stderr, "Done Mapping.")


# from bson import CodecOptions
# with_timezone = CodecOptions(tz_aware=True)


# https://github.com/mongodb/mongo-hadoop/blob/master/streaming/language_support/python/pymongo_hadoop/input.py


# #!/usr/bin/env python
#
# import sys
# import os
# sys.path.append(".")
#
# try:
#     from pymongo_hadoop import BSONMapper
#     import pymongo_hadoop
#     print >> sys.stderr, "pymongo_hadoop is not installed or in path - will try to import from source tree."
# except:
#     here = os.path.abspath(__file__)
#     module_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(here))),
#                     'language_support',
#                     'python')
#     sys.path.append(module_dir)
#     print >> sys.stderr, sys.path
#     from pymongo_hadoop import BSONMapper
#
# def mapper(documents):
#     print >> sys.stderr, "Running python mapper."
#
#     for doc in documents:
#         yield {'_id': doc['_id'].year, 'bc10Year': doc['bc10Year']}
#
#     print >> sys.stderr, "Python mapper finished."
#
# BSONMapper(mapper)



#!/usr/bin/env python

# import sys
# sys.path.append(".")
#
# from pymongo_hadoop import BSONMapper
#
# def mapper(documents):
#     for doc in documents:
#         if 'user' in doc:
#             yield {'_id': doc['user']['time_zone'], 'count': 1}
#
# BSONMapper(mapper)
# print >> sys.stderr, "Done Mapping."