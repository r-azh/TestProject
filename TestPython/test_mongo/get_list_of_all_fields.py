from pprint import pprint
from bson import Code
from pymongo import MongoClient

__author__ = 'R.Azh'


def get_list_of_collection_names(mongo_db_connection):
    return mongo_db_connection.collection_names()


def get_list_of_field_names(mongo_db_connection, collection_name):
    map = Code("function() { for (var key in this) { emit(key, null); }}")
    reduce = Code("function(key, stuff) { return null; }")
    # mr = mongo_db_connection.command({"mapreduce": collection_name,
    #                                                       "map": map, "reduce": reduce, "out": collection_name + "_keys"})
    # return db[mr.result].distinct("_id")
    mr = mongo_db_connection[collection_name].map_reduce(map, reduce, out="_keys")
    return mr.find().distinct("_id")


def get_list_of_fields_data_types(mongo_db_connection, collection_name, field_names):
    if field_names:
        projection = {field_name: {"$type": "${}".format(field_name)} for field_name in field_names}
        projection = {"$project": projection}
        # if don't specify match then gives result for every record
        result = mongo_db_connection[collection_name].aggregate(
            [
               projection
            ])
        # return [dict(t) for t in set([tuple(dict(r.items()).items()) for r in result])]
        # return [dict(k, [[].append(lambda x: x[k], result)]) for k in result[0].keys]
        import collections
        type_dict = collections.defaultdict(set)
        for d in result:
            for k, v in d.items():
                if v != 'missing':
                    type_dict[k].add(v)
        return type_dict


mongo_con = MongoClient('localhost', 27017)
db = mongo_con.ipn
collections = get_list_of_collection_names(db)
print('\n *** list of all collections:\n',)
pprint(collections)
fields = get_list_of_field_names(db, 'person')
print('\n *** list of all fields:\n',)
pprint(fields)
field_types = get_list_of_fields_data_types(db, 'person', fields)
print('\n *** list of all fields:{field types} :\n',)
pprint(field_types)


