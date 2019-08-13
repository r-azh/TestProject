__author__ = 'R.Azh'

# in debugging decorated functions, it can be problematic since the wrapper function does not carry the name,
#  module and docstring of the original function.


def tags(tag_name):
    def tags_decorator(func):
        def func_wrapper(name):
            return "<{0}>{1}</{0}>".format(tag_name, func(name))
        return func_wrapper
    return tags_decorator


@tags("P")
def get_text(name):
    return "Hello " + name

print(get_text("Rezvan"))
print(get_text.__name__)

# The output was expected to be get_text yet, the attributes __name__, __doc__, and __module__ of get_text got
#  overridden by those of the wrapper(func_wrapper. Obviously we can re-set them within func_wrapper but Python
# provides a much nicer way: functools
# functools.wraps. Wraps is a decorator for updating the attributes of the wrapping function(func_wrapper)
#  to those of the original function(get_text).


print("####################### using functools.wraps ######################")
from functools import wraps


def tags_2(tag_name):
    def tags_decorator(func):
        @wraps(func)
        def func_wrapper(name):
            return "<{0}>{1}</{0}>".format(tag_name, func(name))
        return func_wrapper
    return tags_decorator


@tags_2("P")
def get_text(name):
    """returns some text"""
    return "Hello " + name

print(get_text("rezvan"))
print(get_text.__name__)
print(get_text.__module__)
print(get_text.__doc__)