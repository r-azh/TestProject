__author__ = 'R.Azh'
from functools import wraps


def logged(func):
    """ logged """
    def with_logging(*args, **kwargs):
        """ with logging """
        print(func.__name__ + " was called")
        return func(*args, **kwargs)
    return with_logging



@logged
def f(x):
    """ does some math """
    return x + x * x
 ## f = logged(f)

print(f(5))
print(f.__name__)
print(f.__doc__)

######################### with wraps #########################


def logged2(func):
    @wraps(func)
    def with_logging(*args, **kwargs):
        print(func.__name__ + " was called")
        return func(*args, **kwargs)
    return with_logging


@logged2
def f2(x):
    """ does some math """
    return x + x * x

print("\n ----------------")
print(f(6))
print(f2.__name__)
print(f2.__doc__)


