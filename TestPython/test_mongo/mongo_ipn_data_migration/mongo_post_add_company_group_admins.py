from pymongo import MongoClient

__author__ = 'R.Azh'


def add_admin_db():

    dbClient = MongoClient('localhost', 27017)
    db = dbClient.ipn_db

    groups = db.group.find({})
    groups_dict = {}
    for group in groups:
        groups_dict[str(group['_id'])] = [x['person_id'] for x in group['admins']]

    companise = db.company.find({})
    for company in companise:
        groups_dict[str(company['_id'])] = [x['person_id'] for x in company['admins']]

    for key in groups_dict:
        db.post.update({"container_info._id": key}, {"$addToSet": {"container_info.admins": {"$each": groups_dict[
            key]}}}, upsert=False)
    print("admins_added")


add_admin_db()
