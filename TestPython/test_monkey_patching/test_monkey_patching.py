import functools
import types


def foo(arg):
    print("got arg {}".format(arg))


class Bar:
    pass

# __get__ Called to get the attribute of the owner class (class attribute access) or of an
# instance of that class (instance attribute access):  object. __get__(self, instance, owner)
# The descriptor protocol allows to customize how objects behave when they are accessed as attributes of other objects.
#  When you put def statements inside a class statement, Python creates regular functions and set them as attributes of
#  the class, just like it would do for numbers, strings or any other object. It just happens that Python functions
# implement the descriptor protocol and know what to do when they're accessed as class attributes or as instance
# attributes. The intelligence is in the function, not in the class.


print(foo.__get__(Bar(), Bar))
print(foo.__get__(None, Bar))
print(foo.__get__(Bar(), Bar) is foo)
print(foo.__get__(None, Bar) is foo)


# .MethodType can be used to create instance methods or class methods
obj = Bar()
obj.foo = types.MethodType(foo, obj)
obj.foo()

obj.foo = types.MethodType(foo, Bar)
obj.foo()


#  we have a generic tool in the standard library a to create functions that get some of their parameters
# automatically when they're called:

foo42 = functools.partial(foo, 42)
foo42()

obj.foo = functools.partial(foo, obj)
obj.foo()

print(type(obj.foo))
print(isinstance(obj.foo, types.MethodType))