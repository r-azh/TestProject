__author__ = 'R.Azh'

# Variables declared inside the class definition, but not inside a method are class or static variables


class MyClass:
    i = 3

print(MyClass.i)
MyClass.i = 10
#  this creates a class-level "i" variable, but this is distinct from any instance-level "i" variable

m = MyClass()
m.i = 4
print(m.i, MyClass.i)

u = MyClass()
print(u.i)

print(MyClass.__dict__)
print(m.__dict__)
print(u.__dict__)

# You can also add class variables to classes on the fly

MyClass.bar = 0
print(MyClass.bar)

x = MyClass()
print(x.bar)