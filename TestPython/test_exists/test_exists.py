__author__ = 'R.Azh'


class Foo:
    bar = None
    def __init__(self, bar):
        self.bar = bar


o = Foo('a')


class Foo2:
    bar = None
    bar2 = None

x = Foo2()
x.bar = o.bar if hasattr(o, 'bar') else None
x.bar2 = o.bar2 if hasattr(o, 'bar2') else None

print(x.__dict__)

print(hasattr(Foo, 'bar'))