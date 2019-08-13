from pymongo import MongoClient

__author__ = 'R.Azh'

# Define the skeleton of an algorithm in an operation, deferring some steps to subclasses. Template Method lets
# subclasses redefine certain steps of an algorithm without changing the algorithm's structure.


# AbstractClass: defines abstract primitive operations that concrete subclasses define to implement steps of
# an algorithm
# implements a template method defining the skeleton of an algorithm. The template method calls primitive operations as
# well as operations defined in AbstractClass or those of other objects.
class DataAccessObject:
    db_connection = None
    data_set = None
    _db_client = None

    def connect(self):
        self._db_client = MongoClient('localhost', 27017)
        self.db_connection = self._db_client.test_db

    def select(self):
        raise NotImplementedError

    def process(self):
        raise NotImplementedError

    def disconnet(self):
        self._db_client.close()

    def run(self):
        self.connect()
        self.select()
        self.process()
        self.disconnet()


# ConcreteClass: implements the primitive operations ot carry out subclass-specific steps of the algorithm
class Categories(DataAccessObject):
    def select(self):
        collection_source = self.db_connection.categories
        query = {}
        self.data_set = collection_source.find(query)

    def process(self):
        print(" Categories --- ")
        for category in self.data_set:
            print(category["name"])
        print()


class Products(DataAccessObject):
    def select(self):
        collection_source = self.db_connection.products
        query = {}
        self.data_set = collection_source.find(query)

    def process(self):
        print(" Products --- ")
        for product in self.data_set:
            print(product["name"])

# usage
result = MongoClient('localhost', 27017).test_db.products.remove()
products = [{"_id": 1, "name": "Reshnung", "category_id": 1},
            {"_id": 2, "name": "Bildschirm", "category_id": 2}, {"_id": 3, "name": "Laptop", "category_id": 2},
            {"_id": 4, "name": "Computer", "category_id": 2}, {"_id": 5, "name": "Buch", "category_id": 1}]
result = MongoClient('localhost', 27017).test_db.products.insert_many(products)

result = MongoClient('localhost', 27017).test_db.categories.remove()
categories = [{"_id": 1, "name": "Publish"}, {"_id": 2, "name": "Tech"}]
result = MongoClient('localhost', 27017).test_db.categories.insert_many(categories)

doa_categories = Categories()
doa_categories.run()

doa_products = Products()
doa_products.run()
