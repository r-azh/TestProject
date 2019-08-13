import types

__author__ = 'R.Azh'


class Foo:
    def hello(self):
        print("hello")

# without reflection
obj = Foo()
obj.hello()

# with reflection
class_name = "Foo"
method = "hello"
obj = globals()[class_name]()
getattr(obj, method)()

# with eval
eval("Foo().hello()")

###############################
print("######################")


class foo(object):
  def __init__(self, val):
    self.x = val

  def bar(self):
    return self.x

print(dir(foo(5)))

a = foo(10)
b = a.bar()

print(type(a))
print(type(a).__name__)

print(isinstance(a, foo))
print(isinstance(a, type(a)))
print(isinstance(a, type(b)))
print(isinstance(a, types.FunctionType))
print(isinstance(b, types.DynamicClassAttribute))

print(hasattr(a, 'bar'))

###############################
print("######################")


