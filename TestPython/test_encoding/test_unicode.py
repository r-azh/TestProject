__author__ = 'R.Azh'


print('\x80abc'.encode("utf-8", "strict"))

a = 'سلام'
b = '\x80abc'
# in python3 use str instead of unicode: unicode(a)
print(str(b))
print(str(a).encode('utf-8'))
print(a)
