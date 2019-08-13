__author__ = 'R.Azh'

# A generator allows you to write iterators in an elegant succinct syntax that
# avoids writing classes with __iter__() and __next__() methods.

# Any generator also is an iterator (not vice versa!);
# Any generator, therefore, is a factory that lazily produces values.

# There are two types of generators in Python:
# generator functions and
# generator expressions.
# A generator function is any function in which the keyword yield appears in its body.

# The other type of generators are the generator equivalent of a list comprehension.

numbers = [1, 2, 3, 4, 5, 6]
print(numbers)

# list comprehension
l = [x * x for x in numbers]
print(l)

# set comprehension
s = {x * x for x in numbers}
print(s)

# dict comprehension
d = {x: x * x for x in numbers}
print(d)

# generator expression (note: this is not a tuple comprehension)
lazy_squares = (x * x for x in numbers)
print(lazy_squares)
print(next(lazy_squares))
print(list(lazy_squares))


# Tip to get started with generators: find places in your code where you do the following:
#
# def something():
#     result = []
#     for ... in ...:
#         result.append(x)
#     return result
#
# And replace it by:
#
# def iter_something():
#     for ... in ...:
#         yield x
#
# def something():  # Only if you really need a list structure return list(iter_something())
