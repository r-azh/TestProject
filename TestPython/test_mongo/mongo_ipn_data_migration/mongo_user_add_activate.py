from pymongo import MongoClient

__author__ = 'R.Azh'


def copy_user_db():
    def add_activation(documents):
        results = []
        if documents:
            for document in documents:
                document['status'] = 'activated'
                results.append(document)
        return results

    dbClient = MongoClient('localhost', 27017)
    db = dbClient.security_db

    collection = db.user

    users = collection.find({})
    new_users = add_activation(users)
    # result = collection.update({''})
    # print(result.inserted_ids)
    for user in new_users:
        collection.update({"_id": user["_id"]}, user, upsert=False)
    print("users_copied")

copy_user_db()
