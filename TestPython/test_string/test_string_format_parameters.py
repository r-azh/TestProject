import logging
logging.basicConfig(level=logging.INFO)

print('\n###################### format a string using a dictionary ########################\n')

geopoint = {'latitude': 41.123, 'longitude': 71.091}
print('{latitude}, {longitude}'.format(**geopoint))

# or

d = dict(foo='foo', bar='bar', baz='baz')
print('foo is {foo}, bar is {bar} and baz is {baz}'.format_map(d))
print('foo is {foo}, bar is {bar} and baz is {baz}'.format(**d))

a = 'سلام'
b = 'علیک'
print('%(a)s  %(b)s' % {'a': str(a),
                        'b': str(b)})
p1 = {'latitude': 41.123, 'longitude': 71.091}
p2 = {'latitude': 56.456, 'longitude': 23.456}
print('{0[latitude]} {0[longitude]} - {1[latitude]} {1[longitude]}'.format(p1, p2))

# % can't do this
tu = (12, 45, 22222, 103, 6)
print('{0} {2} {1} {2} {3} {2} {4} {2}'.format(*tu))

logging.debug("some debug info: %(this)s and %(that)s", dict(this='Tom', that='Jerry'))


print('\n####################### format a string using a variable ##########################\n')

path = '/path/to/a/file'
print('You put your file here: %(path)s' % locals())


class MyClass:
    def __init__(self):
        self.title = 'Title'

a = MyClass()
print('The title is %(title)s' % a.__dict__)

print('\n#################### format a string using a ANSI C printf format (%) ######################\n')
# %  can either take a variable or a tuple.
sub1 = "python string!"
sub2 = "an arg"
print("i am a %s" % sub1)
print("with %(kwarg)s!" % {'kwarg': sub2})


num = 0
print('number is : %d' % num)

# if num happens to be (1, 2, 3), it will throw a TypeError
num = (1, 2, 3)
print("number is : %s" % (num,))  # supply the single argument as a single-item tuple


print('%(type_names)s [a-z]{2}' % {'type_names': 'triangle|square'})


print('\n###################### format a string using a format() ########################\n')

print("i am a {0}".format(sub1))
print("with {kwarg}!".format(kwarg=sub2))

print("{0} {1} {1}".format("foo", "bar"))


class A(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

a = A(2, 3)
print('x is {0.x}, y is {0.y}'.format(a))


# the old way of formatting strings via % doesn't support Decimal
from decimal import *

getcontext().prec = 50
d = Decimal('3.12375239e-24')  # no magic number, I rather produced it by banging my head on my keyboard

print('%.50f' % d)
print('{0:.50f}'.format(d))

#  you will waste time for logging.debug("something: %s" % x) but not for logging.debug("something: %s", x) The string
# formatting will be handled in the method and you won't get the performance hit if it won't be logged.
x = 'xxxxxxxx'
logging.warning(" something: %s" % x)
logging.warning(" something: %s", x)

print('\n###################### test unicode string ########################\n')

s = 'й'
u = u'й'
print(s)
print(u)
print('%s' % s)
print('%s' % u)
print('{}'.format(s))
print('{}'.format(u))

print('\n###################### use format() as an argument ########################\n')

# send format as an argument to a function
li = [12, 45, 78, 784, 2, 69, 1254, 4785, 984]
print(list(map('the number is {}'.format, li)))


from datetime import datetime, timedelta
once_upon_a_time = datetime(2010, 7, 1, 12, 0, 0)
delta = timedelta(days=13, hours=8,  minutes=20)
gen = (once_upon_a_time + x * delta for x in range(5))
print('\n'.join(map('{:%Y-%m-%d %H:%M:%S}'.format, gen)))


print('\n{0:%Y-%m-%d}'.format(datetime.utcnow()))