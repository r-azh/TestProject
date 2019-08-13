from TestPython.test_datetime.test_datetime_pydal_mongo.mongo.searcher import Searcher

__author__ = 'R.Azh'


class PersonMongoRead(Searcher):
    def __init__(self):
        super(PersonMongoRead, self).__init__("person")


    def get_person_with_birthday(self, from_date, to_date):
        search_query = {"birthday": {"$gt": from_date, "$lt": to_date}}
        return self.collection.reader.find_many()
