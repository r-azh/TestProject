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
        # print(doc)
        yield doc

BSONMapper(mapper)
print(sys.stderr, "Done Mapping.")

