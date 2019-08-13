import importlib

__author__ = 'R.Azh'


m1 = importlib.import_module('TestPython.test_dynamic_import.foo')
print(m1)

# in following way The parent module needs to be imported before trying a relative import.
# You will have to add import 'package' before your call to import_module if you want it to work.
# here it works because its inside the same package
# attention to . in .foo
m2 = importlib.import_module('.foo', package='TestPython.test_dynamic_import')
print(m2)
m3 = importlib.import_module('foo', package='TestPython.test_dynamic_import')
print(m3)

print(m1 is m2)
print(m2 is m3)

my_class = m2.Foo
instance = my_class()
print(instance.__dict__)
my_method = m2.my_method
my_method()

my_class = m3.Foo
instance = my_class()
print(instance.__dict__)
my_method = m3.my_method
my_method()


m4 = importlib.import_module()