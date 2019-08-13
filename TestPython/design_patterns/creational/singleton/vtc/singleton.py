__author__ = 'R.Azh'


class Database(object):
    # single_object = None
    # record = None
    # name = None

    # def __init__(self, name):  ## when called from __new__ dont get arguments
    #     self.name = name
    #     self.record = 0

    # @classmethod
    # def get_instance(cls, name):
    #     if not cls.single_object: ## infinite loop
    #         cls.single_object = Database(name)   ## dont work
    #     return cls.single_object

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "single_object"):
            cls.single_object = super(Database, cls).__new__(cls, *args, **kwargs)
        return cls.single_object

    def __init__(self):
        self.record = 0

    def edit_record(self, operation):
        print("Performing a " + operation +
              " operation on record " + self.record +
              " in database " + self.name)

    ## infinite loop
    # @property
    # def name(self):
    #     return self.name
    #
    # @name.setter
    # def name(self, value):
    #     self.name = value


class DatabaseSynchronized:
    # single_object = None
    # record = None
    # name = None

    # def __init__(self, name):
    #     self.name = name
    #     self.record = 0

    # def get_instance(self, name):
    #     if self.single_object is None:
    #         self.single_object = DatabaseSynchronized(name)
    #     return self.single_object

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "single_object"):
            cls.single_object = super(DatabaseSynchronized, cls).__new__(cls, *args, **kwargs)
        return cls.single_object

    def __init__(self):
        self.record = 0

    def edit_record(self, operation):
        print("Performing a " + operation +
              " operation on record " + self.record +
              " in database " + self.name)

    # @property
    # def name(self):
    #     return self.name


# usage
database = Database()
database.name = "products"
print("This is the " + database.name + " databse.")
print(id(database))

database = Database()
database.name = "employees"
print("This is the " + database.name + " databse.")
print(id(database))


sync_db = DatabaseSynchronized()
sync_db.name = "products"
print("This is the synced " + sync_db.name + " databse.")
print(id(sync_db))

# public class TestSingletonSynchronized implements Runnable
# {
#   Thread thread;
#
#   public static void main(String args[])
#   {
#     TestSingletonSynchronized t = new TestSingletonSynchronized();
#   }
#
#   public TestSingletonSynchronized()
#   {
#     DatabaseSynchronized database;
#
#     database = DatabaseSynchronized.getInstance("products");
#
#     thread = new Thread(this, "second");
#     thread.start();
#
#     System.out.println("This is the " +
#       database.getName() + " database.");
#   }
#
#     public void run()
#     {
#       DatabaseSynchronized database =
#         DatabaseSynchronized.getInstance("employees");
#
#       System.out.println("This is the " +
#         database.getName() + " database.");
#     }
# }