__author__ = 'R.Azh'


def outer():
    x = 1

    def inner():
        print("\n *** inside inner function : ", x)

    return inner()

outer()

print("############## assign functions ##################")


v = outer
v()
print(v.__code__)

print("\n############## function closures ##################")

# . Python supports a feature called function closures which means that inner functions defined in non-global
#  scope remember what their enclosing namespaces looked like at definition time. This can be seen by looking
#  at the func_closure attribute of our inner function which contains the variables in the enclosing scopes.
# The criteria that must be met to create closure in Python are summarized in the following points:
# -We must have a nested function (function inside a function).
# -The nested function must refer to a value defined in the enclosing function.
# -The enclosing function must return the nested function.

print(v.__closure__)


def make_multiplier_of(n):
    def multiplier(x):
        return x * n
    return multiplier

times3 = make_multiplier_of(3)
times5 = make_multiplier_of(5)
print(times5(times3(2)))

# All function objects have a __closure__ attribute that returns a tuple of cell objects if it is a closure function.
#  Referring to the example above, we know times3 and times5 are closure functions.

print(make_multiplier_of.__closure__)
print(times3.__closure__)
print(times5.__closure__)

# The cell object has the attribute cell_contents which stores the closed value.

print(times3.__closure__[0].cell_contents)
print(times5.__closure__[0].cell_contents)

#  closures - the fact that functions remember their enclosing scope - can be used to build custom functions that have,
#  essentially, a hard coded argument.
# And the uses are numerous - if you are familiar with the key parameter in Python’s sorted function you have probably
# written a lambda function to sort a list of lists by the second item instead of the first. You might now be able to
# write an itemgetter function that accepts the index to retrieve and returns a function that could suitably be passed
# to the key parameter.


print("############## pass functions as objects ################")


def add(x, y):
    print(x + y)


def sub(x, y):
    print(x - y)


def apply(func, x, y):
    return func(x, y)

apply(add, 1, 2)
apply(sub, 7, 1)


print("############## return functions from functions ################")


def compose_greet_func():
    def get_message():
        return "Hello there!"

    return get_message

greet = compose_greet_func()
print(greet())