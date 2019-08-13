__author__ = 'R.Azh'
# Python supports an interesting syntax that lets you define one-line mini-functions on the fly
# in lambda functions, if statements are not allowed
# a lambda function is a function that takes any number of arguments (including optional arguments)
# and returns the value of a single expression.
# lambda functions can not contain commands, and they can not contain more than one expression
# a lambda function is always true in a boolean context.
# (That doesn't mean that a lambda function can't return a false value.
# The function is always true; its return value could be anything.)

def f(x):
    return x ^ 2  # xor

print(f(5))

g = lambda x: x ^ 2

print(g(5))

print((lambda x: x ** 2)(3))

collapse = 1
s = "this   is\na\ttest"
processFunc = collapse and (lambda s: " ".join(s.split())) or (lambda s: " :) ".join(s))
print(processFunc(s))

s = "another test"
print(processFunc(s))

print("################################################################################")


def info(object, spacing=10, collapse=1):
    """Print methods and doc strings.

    Takes module, class, list, dictionary, or string."""
    methodList = [method for method in dir(object) if callable(getattr(object, method))]
    processFunc = collapse and (lambda s: " ".join(s.split())) or (lambda s: s)
    print("\n".join(["%s %s" %
                      (method.ljust(spacing),
                       processFunc(str(getattr(object, method).__doc__)))
                     for method in methodList]))

if __name__ == "__main__":
    print(info.__doc__)

print(f.__doc__)

li = []
print(info(li))

print("###############################################################################")

sum = lambda x, y: x + y
print(sum(4, 5))


print("###############################################################################")

# Always use a def statement instead of an assignment statement that binds a lambda expression directly to a name.

# Yes:
def f(x): return 2*x

# No:
f = lambda x: 2*x

# The first form means that the name of the resulting function object is specifically 'f' instead of the generic ''.
#  This is more useful for tracebacks and string representations in general. The use of the assignment statement
#  eliminates the sole benefit a lambda expression can offer over an explicit def statement (i.e. that it can be
# embedded inside a larger expression)
# Assigning lambdas to names basically just duplicates the functionality of def - and in general, it's best to do
#  something a single way to avoid confusion and increase clarity.

# The legitimate use case for lambda is where you want to use a function without assigning it, e.g:
#
# sorted(players, key=lambda player: player.rank)