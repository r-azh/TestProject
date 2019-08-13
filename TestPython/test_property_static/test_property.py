from bson import ObjectId

__author__ = 'R.Azh'

# Partial expected static variable behavior, i.e., syncing of the attribute between multiple instances
# (but not with the class itself; see "gotcha" below), can be achieved by turning the class attribute into a property:


class Class1(object):
    _i = 3

    @property
    def i(self):
        return self._i

    @i.setter    # @property must be defined earlier to recognize i
    def i(self, val):
        self._i = val

# ALTERNATIVE IMPLEMENTATION - FUNCTIONALLY EQUIVALENT TO ABOVE ##
# (except with separate methods for getting and setting i) ##


class Class2(object):
    _i = 3

    def get_i(self):
        return self._i

    def set_i(self, val):
        self._i = val

    i = property(get_i, set_i)

x1 = Class2()
x2 = Class2()
x1.i = 50
x3 = Class2()
print(x1.i)
print(x2.i)
print(x3.i)

Class2.i = 99
x4 = Class2()
print(x1.i)
print(x2.i)
print(x4.i)
# For immutable static variable behavior, simply omit the property setter.

print("\n#################### property complete sample ##################")


class C(object):
    def __init__(self):
        self._x = None

    def getx(self):
        return self._x

    def setx(self, value):
        self._x = value

    def delx(self):
        del self._x

    x = property(getx, setx, delx, "I'm the 'x' property.")


class CPlus(object):
    def __init__(self):
        self._x = None

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @x.deleter
    def x(self):
        del self._x


print("\n#################### some points ##################")


def getter(self):
    print("Get!")


def setter(self, value):
    print('Set to {!r}!'.format(value))


def deleter(self):
    print('Delete!')

prop = property(getter)
print(prop.fget is getter)
print(prop.fset is None)
print(prop.fdel is None)

prop = prop.setter(setter)
print(prop.fget is getter)
print(prop.fset is setter)
print(prop.fdel is None)

prop = prop.deleter(deleter)
print(prop.fget is getter)
print(prop.fset is setter)
print(prop.fdel is deleter)

# the property object acts as a descriptor object, so it has .__get__(), .__set__() and
# .__delete__() methods to hook into instance attribute getting, setting and deleting:


class Foo(object):
    pass

prop.__get__(Foo(), Foo)
prop.__set__(Foo(), 'bar')
prop.__delete__(Foo())

prop.__get__(C(), C.x)
prop.__set__(C(), 'bar')
prop.__delete__(C())

print('\n###################### property in inheritance ###################')


class Human(object):
    def __init__(self, name=''):
        self._name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value


class SuperHuman(Human):
    @Human.name.getter              #@property :  Doesn't work :( "AttributeError: can't set attribute"
    def name(self):
        return 'super {}'.format(str(self._name))

s = SuperHuman('john')
print(s.name)

s.name = 'jack'
print(s.name)


