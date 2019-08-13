__author__ = 'R.Azh'


class A(object):
    def __init__(self):
        self.y = 0

    class B(object):
        def __init__(self):
            self.x = 0

        def f(self):
            pass


obj = A.B()
obj.f()


class Outer(object):
    outer_var = None

    def __init__(self):
        self.outer_var = 1

    def get_inner(self):
        return self.Inner(self)
        # "self.Inner" is because Inner is a class attribute of this class
        # "Outer.Inner" would also work, or move Inner to global scope
        # and then just use "Inner"

    class Inner(object):
        def __init__(self, outer):
            self.outer = outer

        @property
        def inner_var(self):
            return self.outer.outer_var

    class Inner2(object):
        @property
        def inner_var(self):
          return Outer.outer_var

print(Outer.Inner(Outer()).inner_var)
print(Outer.Inner2().inner_var)


