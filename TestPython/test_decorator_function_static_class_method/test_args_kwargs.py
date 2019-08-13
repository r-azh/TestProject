__author__ = 'R.Azh'

#  the * operator used when defining a function means that any extra positional arguments passed to the
#  function end up in the variable prefaced with a *

print("\n################ * in defining functions ####################")


def f1(*args):
    print(args)

f1()
f1(1, 2, 3)


def f2(x, y, *args):
    print(x, y, args)

f2(1, 2)
f2('a', 'b', 'c')


print("\n################ * in calling functions ####################")
# The * operator can also be used when calling functions. A variable prefaced by * when calling a function means
#  that the variable contents should be extracted and used as positional arguments


def add(x, y):
    print(x + y)


lst = [1, 2]
add(lst[0], lst[1])

add(*lst)

print("\n################ ** in defining functions ####################")
# ** which does for dictionaries & key/value pairs exactly what * does for iterables and positional parameters


def foo(**kwargs):
    print(kwargs)

foo()
foo(x=1, y=2)

# neither the name args nor kwargs is part of Python syntax but it is convention to use these variable
# names when declaring functions.

print("\n################ ** in calling functions ####################")

dct = {'x': 1, 'y': 2}


def bar(x, y):
    print(x + y)

bar(**dct)