__author__ = 'R.Azh'

# An iterable is any object, not necessarily a data structure, that can
# return an iterator (with the purpose of returning all of its elements).
# most containers are also iterable. But many more things are iterable as well.
#  Examples are open files, open sockets, etc. Where containers are typically
#  finite, an iterable may just as well represent an infinite source of data.

x = [1, 2, 3]
y = iter(x)
z = iter(x)
print(next(y))
print(next(y))
print(next(z))

print(type(x))
print(type(y))


# Often, for pragmatic reasons, iterable classes will implement both __iter__()
# and __next__() in the same class, and have __iter__() return self,
#  which makes the class both an iterable and its own iterator.
# It is perfectly fine to return a different object as the iterator, though.

import dis

dis.dis('for _ in x: pass')

# When dealing with iterators you have to remember that they are stateful and that they mutate as you traverse them.
# Lists are more predictable since they only change when you explicitly mutate them; they are containers.
