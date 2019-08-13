__author__ = 'R.Azh'

# Static method can access classes static variables


class StaticMClass:
    @staticmethod
    def f():
        print("static method")

StaticMClass.f()