__author__ = 'R.Azh'


a_string = "This is a global variable"


def foo():
    print(locals())

foo()
print(globals())


def foo2():
    print(locals())
    a_string = "test"   # actually creating a new local variable that "shadows" the global variable with the same name.
    print(locals())

foo2()
print(globals())


