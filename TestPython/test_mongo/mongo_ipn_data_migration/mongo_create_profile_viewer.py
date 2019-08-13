from pymongo import MongoClient

__author__ = 'R.Azh'


def create_profile_viewer():
    def create_pv_documents(documents):
        results = []
        if documents:
            for document in documents:
                results.append(create_pv_document(document))
        return results

    def create_pv_document(viewer):
        dict = {"_id": viewer["_id"],
                "py/object": "parsadp.ipn.domain.aggregates.person.model.profile_viewer.ProfileViewer",
                "viewers": []}
        return dict

    dbClient = MongoClient('localhost', 27017)
    db = dbClient.ipn_db

    collection_source = db.person
    collection_target = db.profile_viewer

    users = collection_source.find({})
    viewers_documents = create_pv_documents(users)
    result = collection_target.insert_many(viewers_documents)
    print(result.inserted_ids)
    print("users_copied")
    dbClient.close()

create_profile_viewer()