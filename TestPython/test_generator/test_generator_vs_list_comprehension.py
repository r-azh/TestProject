__author__ = 'R.Azh'

# Sometimes you have to use generators for example if you're writing coroutines with cooperative scheduling using yield.

# Use list comprehensions when the result needs to be iterated over multiple times,
# or where speed is paramount. (paramount: more important than anything else; supreme)
# you should use a list if you want to use any of the list methods.
# Use generator expressions where the range is large or infinite.
# Basically, use a generator expression if all you're doing is iterating once.
# If you want to store and use the generated results, then you're probably better off with a list comprehension.
# The important point is that the list comprehension creates a new list.
# The generator creates a an iterable object that will "filter" the source material on-the-fly as you consume the bits.

# Generator expression
print(x*2 for x in range(51))

# List comprehension
print([x*2 for x in range(51)])

def gen():
    return (something for something in get_some_stuff())

# print(gen()[:5])     # generators don't support indexing or slicing
# print([5,6] + gen()) # generators can't be added to lists

list = [x*2 for x in range(51)]
print([list[:5]])
print([5,6] + list)

# generators (and any iterable) can be added to lists with extend
a = (x for x in range(0,10))
b = [1, 2, 3]
print(b.extend(a))  # will evaluate all of a, in which case there's no point in making it a generator in the first place.
# a.extend(b) # throws an exception

