import sys
sys.path.insert(0, '/var/www/venv/IPN-Core')
sys.path.insert(0, '/var/www/venv/IPN-App/IPN')

from pymongo import MongoClient
from parsadp.ipn.domain.aggregates.person.model.relation import Relation

__author__ = 'R.Azh'


def add_relation_to_db():

    def create_relation_list(documents):
        results = []
        if documents:
            for document in documents:
                person_relation = Relation()
                person_relation._id = document['_id']
                results.append(person_relation)
        return results

    dbClient = MongoClient('localhost', 27017)
    db = dbClient.ipn_db

    users = db.person.find({})
    relations = db.relation.find({})
    relation_ids = []
    if relations:
        for r in relations:
            print(r)
            relation_ids.append(str(r['_id']))

    new_relations = create_relation_list(users)
    if new_relations:
        for relation in new_relations:
            if str(relation._id) not in relation_ids:
                result = relation.create()
                print(result)

add_relation_to_db()