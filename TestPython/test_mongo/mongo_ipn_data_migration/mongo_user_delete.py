from pymongo import MongoClient

__author__ = 'R.Azh'

# def delete_user(user_id):
#     dbClient = MongoClient('localhost', 27017)
#     sec_db = dbClient.security_db
#     ipn_db = dbClient.ipn_db
#
#     user = sec_db.user.find_one({"_id": user_id})
#     print(user)
#     # result = sec_db.user.delete_one({"_id": user_id})
#     # print(result.deleted_count)
#
#     person = ipn_db.person.find_one({"_id": user_id})
#     print(person)
#     # result = ipn_db.person.delete_one({"_id": user_id})
#     # print(result.deleted_count)