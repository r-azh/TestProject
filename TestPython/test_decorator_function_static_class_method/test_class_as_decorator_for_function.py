__author__ = 'R.Azh'


class Foo:
    def __init__(self, func):
        """
        If there are no decorator arguments, the function
        to be decorated is passed to the constructor.
        """
        self.func = func

    def __call__(self, *args):
        """
        The __call__ method is not called until the
        decorated function is called.
        """
        print("make class Foo callable for using as decorator")
        print(*args)
        self.func(*args)


@Foo
def f(a):
    print(a)

f("hi")

