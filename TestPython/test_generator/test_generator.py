# in functions (more generally referred to as subroutines in computer programming) "return", implies that
# the function is returning control of execution to the point where the function was called.
# "Yield", implies that the transfer of control is temporary and voluntary, and our function expects
# to regain it in the future. In Python, "functions" with these capabilities are called "generators".

# Note: Outside of Python, all but the simplest generators would be referred to as coroutines.
# The important thing to remember is, in Python, everything described here as a coroutine is still a generator.

# A generator function is defined like a normal function, but whenever it needs to generate a value,
# it does so with the yield keyword rather than return. If the body of a def contains yield, the function
#  automatically becomes a generator function (even if it also contains a return statement).

# Just remember that a generator is a special type of iterator

# In Python a generator can be used to let a function return a list of values without having to
#  store them all at once in memory. This also allows you to utilize the values immediately
#  without having to wait until all values have been computed.


def simple_generator_function():
    yield 1
    yield 2
    yield 3

for value in simple_generator_function():
    print(value)

our_generator = simple_generator_function()
print(next(our_generator))
print(next(our_generator))
print(next(our_generator))
# print(next(our_generator))   # doesn't work anymore
for value in our_generator:  # doesn't work anymore
    print(value)

new_generator = simple_generator_function()
for value in new_generator:  # works just fine
    print(value)

# When a generator function calls yield, the "state" of the generator function is frozen;
#  the values of all variables are saved and the next line of code to be executed is recorded
# until next() is called again. Once it is, the generator function simply resumes where it left off.

# One would expect to be able to create a tuple using the usual comprehension syntax, e.g.
# (i for i in range(10)) but the value of this expression is not a tuple. It is a generator
# one can write a comprehension over a generator instead of over a list or set or
# tuple. Alternatively, one can use set(·) or list(·) or tuple(·) to transform a generator
# into a set or list or tuple.
print('\n###################### send / next #########################\n')
print("check test_generator_send_next")
print('\n###################### yield from ##########################\n')
# it enables you to easily refactor a generator by splitting it up into multiple generators.


def generator():
    for i in range(10):
        yield i
    for j in range(10, 20):
        yield j

print(generator())
for value in generator():
    print(value)


def generator2():
    for i in range(10):
        yield i


def generator3():
    for j in range(10, 20):
        yield j


def generator_refactored():
    for i in generator2():
        yield i
    for j in generator3():
        yield j

for value in generator_refactored():
    print(value)

print('\n###################### using yield from ##########################\n')


def generator_refactored_yield_from():
    yield from generator2()
    yield from generator3()

for value in generator_refactored_yield_from():
    print(value)

print('\n###################### using itertools chain ##########################\n')

from itertools import chain


def generator_itertools():
    for v in chain(generator2(), generator3()):
        yield v

for value in generator_itertools():
    print(value)








