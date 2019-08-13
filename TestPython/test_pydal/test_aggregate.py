from pymongo import MongoClient


from pydal.mongo.connection import Connection

pydalConnection = Connection("mongodb://localhost:27017")
pydalCollection = pydalConnection \
    .db("ipn_db") \
    .collection("group_post")

#  gives all the files of all posts in a group
query = [{"$match":
         {"group_id": "5729a5c23ae7281ecf21e632"}},
         {"$project": {
             "file": {
                 "$map": {
                     "input": {"$literal": ["p1", "p2"]},
                         "as": "p",
                         "in": {
                             "$cond": [
                                 {"$eq": ["$$p", "p1"]},
                                 "$file",
                                 "$file_thumbnail"]}
                     }
             }
             }},
         {"$unwind": "$file"}]

# query = [{"$match":
#          {"group_id": "5729a5c23ae7281ecf21e632"}},
#          {"$project": {
#              "_id": 1,
#              "py/object": 1,
#              "file": {
#                  "$map": {
#                      "input": {"$literal": ["p1", "p2"]},
#                          "as": "p",
#                          "in": {
#                              "$cond": [
#                                  {"$eq": ["$$p", "p1"]},
#                                  "$file",
#                                  "$file_thumbnail"]}
#                      }
#              }
#              }},
#          {"$unwind": "$file"}]
#
# query = [{"$unwind": "$file"},
#          {"$match": {"group_id": "5729a5c23ae7281ecf21e632"}}]
result = pydalCollection.reader.aggregate(fields=["file", "_id"], query=query, skip=None, take=None)
print(result)
for row in result:
    print(row)

print('\n########## using pymongo #############\n')

dbClient = MongoClient('localhost', 27017)
db = dbClient.ipn_db
collection_source = db.group_post
result = collection_source.aggregate(query)
for row in result:
    print(row)
print(result)
