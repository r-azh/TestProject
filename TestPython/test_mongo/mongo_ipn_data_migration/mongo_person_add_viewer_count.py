from pymongo import MongoClient

__author__ = 'R.Azh'


def copy_user_db():
    def add_viewer_count(documents):
        results = []
        if documents:
            for document in documents:
                document['viewer_count'] = 0
                results.append(document)
        return results

    dbClient = MongoClient('localhost', 27017)
    db = dbClient.ipn_db

    collection = db.person

    users = collection.find({})
    new_users = add_viewer_count(users)
    for user in new_users:
        collection.update({"_id": user["_id"]}, user, upsert=False)
    print("users_copied")

copy_user_db()


# db.getCollection('person').update({}, {'$set': {'viewer_count': 0}}, {'multi':true})
