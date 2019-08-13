from pprint import pprint
from bson import ObjectId
from pymongo import MongoClient

__author__ = 'R.Azh'


def resolve_inconsistency_in_post_viewer_count():
    uri = "mongodb://localhost:27017"
    dbClient = MongoClient(uri)
    print(dbClient.database_names())
    db = dbClient.ipn

    list_id_count = db.post_visit_log.aggregate([{'$match': {'read_state': True}},
                                                 {'$group': {'_id': '$visited_item_id', 'count': {'$sum': 1}}}])
    result = db.post.update({}, {"$set": {"viewer_count": 0}}, multi=True)
    print(result)
    if list_id_count:
        for l in list_id_count:
            pprint(l)
            result = db.post.update({"_id": ObjectId(l['_id'])},
                                    {"$set": {"viewer_count": l['count']}})
            print(result)
    print("inconsistencies_resolved")


resolve_inconsistency_in_post_viewer_count()


# db.getCollection('person').update({}, {'$set':{'experiences':[], 'following_groups':[], 'following_companies':[]}}, false, true)
