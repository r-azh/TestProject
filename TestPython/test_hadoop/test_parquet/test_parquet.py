from pprint import pprint
from pymongo import MongoClient

__author__ = 'R.Azh'

# https://arrow.apache.org/docs/python/parquet.html

# The Apache Parquet project provides a standardized open-source columnar storage format for use in data analysis
# systems.
# Apache Arrow is an ideal in-memory transport layer for data that is being read or written with Parquet files.
# pandas is an open source, BSD-licensed library providing high-performance, easy-to-use data structures and data
# analysis tools for the Python programming language.

import numpy as np
import pandas
import pyarrow
import pyarrow.parquet as pq

data_frame = pandas.DataFrame({'one': [-1, np.nan, 2.5], 'two': ['foo', 'bar', 'baz'], 'three': [True, False, True]},)
table = pyarrow.Table.from_pandas(data_frame)
pq.write_table(table, 'example.parquet')


# This creates a single Parquet file. In practice, a Parquet dataset may consist of many files in many directories. We
# can read a single file back with read_table:

table2 = pq.read_table('example.parquet')
print(table2.to_pandas())

# You can pass a subset of columns to read, which is faster than reading the whole file (due to the columnar layout):
r = pq.read_table('example.parquet', columns=['one', 'three'])
print(r)
print(r.to_pandas())

parquet_file = pq.ParquetFile('example.parquet')
print('\nmetadata:\n', parquet_file.metadata)
print('\nschema:\n', parquet_file.schema)

# Parquet file consists of multiple row groups. read_table will read all of the row groups and concatenate them
# into a single table. You can read individual row groups with read_row_group
print('\nnum row groups:\n', parquet_file.num_row_groups)

print('\nrow group:\n', parquet_file.read_row_group(0))

# We can write a Parquet file with multiple row groups by using ParquetWriter
writer = pq.ParquetWriter('example2.parquet', table.schema)
for i in range(3):
    writer.write_table(table)
writer.close()

pf2 = pq.ParquetFile('example2.parquet')
print('\nnum row groups:\n', pf2.num_row_groups)


# append

pq.write_table(table, 'example.parquet')
table2 = pq.read_table('example.parquet')
print(table2.to_pandas())

mongo_con = MongoClient('localhost', 27017)
db = mongo_con['ipn']
result = db.person.find_one({})
if result:
    doc = result
    col = list(result)
    pprint(doc)
    print(col)
    data_frame = pandas.DataFrame.from_dict(col)
    print('data frame:\n', data_frame)
    # table2 = pyarrow.Table.from_pandas(data_frame)
    # print(table2)

data_frame2 = pandas.DataFrame(list(db.person.find({}).limit(10)))

print(data_frame2)