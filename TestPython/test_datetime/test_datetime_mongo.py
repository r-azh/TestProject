import datetime

__author__ = 'R.Azh'

import pymongo
client = pymongo.MongoClient('localhost', 27017)
db = client.test_db
col = db.test_date_collection


def insert_date_as_string():
    col.insert({'start_date': '2001-4-5','end_date': '2015-4-5'})
    col.insert({'start_date': '2001-3-5','end_date': '2015-3-5'})
    col.insert({'start_date': '2001-7-5','end_date': '2015-6-5'})
    col.insert({'start_date': '2001-9-5','end_date': '2015-6-5'})
    col.insert({'start_date': '2001-8-5','end_date': '2015-6-5'})


def find_date_as_string():
    cursor = col.find({'start_date': {"$gte": "2001-04-29",
                                      "$lt": "2015-05-01"}})
    print('Found', cursor.count())
    for document in cursor:
        print(document)

insert_date_as_string()
find_date_as_string()


def insert_date_as_isodate():
    col.insert({'start_date': 'ISODate("2000-04-30T00:00:00.000Z")', 'end_date': 'ISODate("2010-04-30T00:00:00.000Z")'})
    col.insert({'start_date': 'ISODate("2000-04-30T00:00:00.000Z")', 'end_date': 'ISODate("2010-04-30T00:00:00.000Z")'})
    col.insert({'start_date': 'ISODate("2000-04-30T00:00:00.000Z")', 'end_date': 'ISODate("2010-04-30T00:00:00.000Z")'})
    col.insert({'start_date': 'ISODate("2000-04-30T00:00:00.000Z")', 'end_date': 'ISODate("2010-04-30T00:00:00.000Z")'})
    col.insert({'start_date': 'ISODate("2000-04-30T00:00:00.000Z")', 'end_date': 'ISODate("2010-04-30T00:00:00.000Z")'})


def find_date_as_isodate():
    cursor = col.find({'start_date': {"$gte": "ISODate(\"2000-03-29T00:00:00.000Z\")",
                                      "$lt": "ISODate(\"2015-05-01T00:00:00.000Z\")"}})
    print('Found', cursor.count())
    for document in cursor:
        print(document)


# db.getCollection('group_post').find(
#     {'$and':
#            [{'publish_datetime':{'$lt': '2016-10-03T00:00:00.000000'}}, {'publish_datetime':{'$gt':'2016-10-01T00:00:00.000000'}}]})

insert_date_as_isodate()
find_date_as_isodate()


client.close()

col.insert({'start_date': datetime.datetime.utcnow(), 'end_date': datetime.datetime.utcnow()})
date1 = datetime.datetime.utcnow() - datetime.timedelta(minutes=15)
cursor = col.find({'start_date': {"$gte": date1}})
print('Found', cursor.count())
for document in cursor:
    print(document)


