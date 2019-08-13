__author__ = 'R.Azh'


class some_class:
    property = None


a = some_class()
a.property = 'x'

if hasattr(a, 'property'):
   print(a.property)
