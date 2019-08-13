from bson import ObjectId
from pymongo import MongoClient

__author__ = 'R.Azh'
import sys

sys.path.insert(0, '/var/www/venv/IPN-Core')
sys.path.insert(0, '/var/www/venv/IPN-App/IPN')


def copy_user_db():
    def add_activation(documents):
        from parsadp.ipn.domain.aggregates.user_account.model.user_account import UserAccount

        results = []
        if documents:
            for document in documents:
                user = UserAccount()
                user._id = document['_id']
                user.user_name = document['user_name']
                user.password = document['password']
                user.status = 'enabled'
                user._is_sys_admin = True if user._id == ObjectId('560121abcbf62c13d4567f0d') or user._id == ObjectId('580e04a33ae7280ae09d93a5') else False
                results.append(user)
        return results

    dbClient = MongoClient('localhost', 27017)

    users = dbClient.security_db.user.find({})
    new_users = add_activation(users)

    from parsadp.ipn.domain.aggregates.user_account.app.v1_0.rest.assembler import user_account_writer

    for user in new_users:
        user_account_writer.create(user)    # password wont be copied by pydal
        # dbClient.ipn_db.user_account.update({"_id": ObjectId(user.__dict__['_id'])}, {"password": user.__dict__['password']}, upsert=False) # keeps only id and password
        # dbClient.ipn_db.user_account.update({"_id": ObjectId(user.__dict__['_id'])},  user.__dict__, upsert=False) # dont work
        dbClient.ipn_db.user_account.update({"_id": ObjectId(user.__dict__['_id'])},  {'$set': {'password': user.__dict__['password']}}, upsert=False)
    print("{} users_copied".format(len(new_users)))

copy_user_db()