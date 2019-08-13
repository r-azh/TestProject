__author__ = 'R.Azh'

tu = ("1", "a", 30)
print(isinstance(tu, tuple))

print(isinstance([], list))

print(isinstance({}, dict))


class Class1(object):
    pass


class Class2(Class1):
    pass

a = Class1()
b = Class2()
print(isinstance(a, Class1))
print(isinstance(b, Class1))
print(isinstance(b, Class2))

print(type(a) is Class1)
print(type(a))

print('############### function type ##################')


def func():
    pass

print(func.__class__)

print('############### issubclass ##################')
print(issubclass(func.__class__, object))