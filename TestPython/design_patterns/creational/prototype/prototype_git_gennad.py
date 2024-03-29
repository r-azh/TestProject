from copy import deepcopy, copy


copyfunc = deepcopy


def Prototype(name, bases, dict):
    class Cls:
        pass
    Cls.__name__ = name
    Cls.__bases__ = bases
    Cls.__dict__ = dict
    inst = Cls()
    inst.__call__ = Copyier(inst)
    return inst


class Copyier:
    def __init__(self, inst):
        self._inst = inst

    def __call__(self):
        newinst = copyfunc(self._inst)
        if copyfunc == deepcopy:
            newinst.__call__._inst = newinst
        else:
            newinst.__call__ = Copyier(newinst)
        return newinst


class Point:
    __metaclass__ = Prototype
    x = 0
    y = 0

    @classmethod
    def move(self, x, y):
        self.x += x
        self.y += y


a = Point()
print(a.x, a.y)          # prints 0 0
a.move(100, 100)
print(a.x, a.y)          # prints 100 100

Point.move(50, 50)
print(Point.x, Point.y)

print(Point.x, Point.y)  # prints 50 50
p = Point()
print(p.x, p.y)          # prints 50 50

q = p
print(q.x, q.y)          # prints 50 50
