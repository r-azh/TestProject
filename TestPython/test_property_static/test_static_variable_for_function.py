__author__ = 'R.Azh'

# You can add attributes to a function, and use it as a static variable.


def myfunc():
    myfunc.counter += 1
    print(myfunc.counter)


# attribute must be initialized
myfunc.counter = 0
myfunc()
myfunc()
myfunc()

print("\n################ init inside function #################")
# if you don't want to setup the variable outside the function


def myfunc2():
    if not hasattr(myfunc2, "counter"):
        myfunc2.counter = 10  # it doesn't exist yet, so initialize it
    myfunc2.counter += 1
    print(myfunc2.counter)

# or


def myfunc3():
    try:
        myfunc3.counter += 1
    except AttributeError:
        myfunc3.counter = 1

myfunc2()
myfunc2()
myfunc2()

print("\n################# using decorator #################\n")
# If you want the counter initialization code at the top instead of the bottom, you can create a decorator:


def static_vars(**kwargs):
    def decorate(func):
        for k in kwargs:
            setattr(func, k, kwargs[k])
        return func
    return decorate


@static_vars(counter=1000)
def foo():
    foo.counter += 1
    print("Counter is %d" % foo.counter)

foo()
foo()
foo()
foo()