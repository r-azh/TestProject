
__author__ = 'R.Azh'


# in cases where you want to import a module whose name is only known at runtime use __import__

# When the 'name' parameter is of the form package.module, normally, the top-level package (the name up till the first
# dot) is returned, not the module named by name.
module = __import__('TestPython.test_dynamic_import.foo')
# my_class = getattr(module, 'Foo')        # gives error


# However, when a non-empty 'fromlist' argument is given, the module named by name is returned.
module = __import__('TestPython.test_dynamic_import.foo', globals(), locals(), ['Foo', 'my_method'])
my_method = getattr(module, 'my_method')
my_method()
my_class = getattr(module, 'Foo')
instance = my_class()
print(instance.__dict__)

my_class = module.Foo
instance = my_class()
print(instance.__dict__)
my_method = module.my_method
my_method()

# If you simply want to import a module (potentially within a package) by name, use importlib.import_module().