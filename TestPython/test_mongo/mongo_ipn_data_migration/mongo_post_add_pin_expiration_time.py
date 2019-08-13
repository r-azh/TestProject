from pymongo import MongoClient

__author__ = 'R.Azh'


def add_pin_expiration_datetime():

    dbClient = MongoClient('localhost', 27017)
    db = dbClient.ipn_db

    posts = db.post.find({})
    # for post in posts:
    #     post['pin_expiration_datetime'] = post['publish_datetime']

    for post in posts:
        db.post.update({"_id": post['_id']}, {"$set": {"pin_expiration_datetime": post['publish_datetime']}},
                       upsert=False)
    print("pin_expiration_time_added")


add_pin_expiration_datetime()
