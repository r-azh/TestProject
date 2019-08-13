import sys

__author__ = 'R.Azh'

# getattr is an incredibly useful built-in function that returns any attribute of any object
# getattr(object, "attribute") is equivalent to object.attribute.
li = ["Larry", "Curly"]
print(li.pop())
print(getattr(li, "pop"))

getattr(li, "append")("Moe")  # equals: li.append("Moe")
print(li)

getattr({}, "clear")
print(li)

import pymongo
import types

print(type(getattr(pymongo, "InsertOne")))
print(type(getattr(pymongo, "InsertOne")) == types.MethodType)

print("######### call a function from string name of function ############")


class Foo:
    att = 10

    def bar(self):
        print("foo.bar")

method = getattr(Foo, 'bar')
result = method(Foo)        # using Foo instead of self in bar(self)

class_name = getattr(sys.modules[__name__], "Foo")
result = class_name().bar()

class_name = eval("Foo")
result = class_name().bar()

attribute = getattr(Foo, 'att')
print(attribute)

print(vars(Foo))


print(Foo.__module__)
print(Foo.__qualname__)