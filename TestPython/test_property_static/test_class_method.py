__author__ = 'R.Azh'

# The @staticmethod allows you only to access the static variables in the same class.
#  With the @classmethod you’ll be able to modify class variables of the subclasses
# without the neccessity of redefining the method when using inheritance.


class ClassMethod(object):
    i = 3   # class (or static) variable

    @classmethod
    def g(cls, arg):
        # here we can use 'cls' instead of the class name (Test)
        if arg > cls.i:
            cls.i = arg     # would the the same as  Test.i = arg1
        print(cls.i)

ClassMethod.g(7)