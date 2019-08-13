__author__ = 'R.Azh'

# The advantage of using a with statement is that it is guaranteed to close
# the file no matter how the nested block exits. If an exception occurs before
# the end of the block, it will close the file before the exception is caught
# by an outer exception handler. If the nested block were to contain a return
#  statement, or a continue or break statement, the with statement would
# automatically close the file in those cases, too.


with open('output.txt', 'w') as f:
    f.write('Hi there!')

from os.path import dirname
print(dirname(__file__))

# File objects expose their own __enter__ and __exit__ methods, and can therefore
# act as their own context managers. Specifically, the __exit__ method closes the file.

# There are two ways to support the with statement:
#  by implementing a context manager class,
# or by writing a generator function.


class DatabaseConnection(object):
    dbconn = None

    def __enter__(self):
        # make a database connection and return it
        return self.dbconn

    def __exit__(self, exc_type, exc_val, exc_tb):
        # make sure the dbconnection gets closed
        self.dbconn.close()


with DatabaseConnection() as mydbconn:
    # do stuff
    pass