__author__ = 'R.Azh'


class new_class():
    def __init__(self, number):
        self.multi = int(number) * 2
        self.str = str(number)

a = new_class(2)
print(a.__dict__)
# {'multi': 4, 'str': '2'}
print(a.__dict__.keys())
# dict_keys(['multi', 'str'])

##############################


class MyClass(object):
    a = '12'
    b = '34'

    def myfunc(self):
        return self.a


import inspect
attributes = inspect.getmembers(MyClass, lambda a: not(inspect.isroutine(a)))
print(attributes)
att_value_list = [a for a in attributes if not(a[0].startswith('__') and a[0].endswith('__'))]
print(att_value_list)

att_list = [a[0] for a in attributes if not(a[0].startswith('__') and a[0].endswith('__'))]
print("\natt_list:", att_list)

print(MyClass.__dict__.keys())
print(dir(MyClass))
