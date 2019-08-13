__author__ = 'R.Azh'


class bar(object):
    def __init__(self):
        self.val = 4

    def setVal(self, x):
        self.val = x

    @staticmethod
    def decor(func):
        def increment(self, x):
            return func(self, x) + self.val
        return increment


class foo(bar):
    def __init__(self):
        bar.__init__(self)

    @bar.decor
    def add(self, x):
        return x


#---------------------------------------------

def memoized(func):
    def fun(cls, arg):
        print(cls, arg)
        print('in memo')
    return fun


class A:
    @memoized
    def fun(self, arg):
        print('in parent')


class B(A):
    def fun(self, arg):
        print('in subclass')

b = B()
b.fun(1)

a = A()
a.fun(2)