from flask.ext.bcrypt import Bcrypt
from pymongo import MongoClient

__author__ = 'R.Azh'
# todo: mongo
# todo: db.copyDatabase('old_security_db', 'security_db')
# todo: use security_db
# todo: db.dropDatabase()
# todo: db.copyDatabase('ipn_db', 'old_ipn_db')
# todo: use ipn_db
# todo: db.dropDatabase()
# todo: dont delete messaging_db
# todo: dont delete person_files
# todo: dont delte proficiency_endorser
# db.copyDatabase('old_security_db', 'security_db')


def copy_user_db():
    def hash_results(documents):
        results = []
        if documents:
            for document in documents:
                results.append(hash_result(document))
        return results

    def hash_result(user):
        bcrypt = Bcrypt(None)
        password_hash = bcrypt.generate_password_hash(user["password"])
        user["password"] = password_hash
        return user

    dbClient = MongoClient('localhost', 27017)
    old_db = dbClient.old_security_db
    new_db = dbClient.security_db

    collection_source = old_db.user
    collection_target = new_db.user

    users = collection_source.find({})
    new_users = hash_results(users)
    result = collection_target.insert_many(new_users)
    print(result.inserted_ids)
    # for user in new_users:
    #     collection_target.update({"_id": user["_id"]}, user)
    print("users_copied")


def copy_person_db():
    def convert_results(documents):
        results = []
        if documents:
            for document in documents:
                results.append(convert_result(document))
        return results

    def convert_result(person):
        person["following_groups"] = []
        # person["proficiencies"] = []
        return person

    dbClient = MongoClient('localhost', 27017)
    old_db = dbClient.old_ipn_db
    new_db = dbClient.ipn_db

    collection_source = old_db.person
    collection_target = new_db.person

    persons = collection_source.find({})
    new_users = convert_results(persons)
    result = collection_target.insert_many(new_users)
    print(result.inserted_ids)
    print("persons_copied")

copy_user_db()
# copy_person_db()