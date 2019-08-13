from functools import wraps

__author__ = 'R.Azh'


def a():
    def b():
        print("in b")
    return b


a()  # returns b but don't run it
a()()  # run b


print("####### test decorator: cc wont be called if we don't call it in decorator #########")


def aa(func):
    def bb():
        print("in bb")
    return bb

# decorated by aa
@aa
def cc():
    print("in cc")

cc()

print("####### test decorator #########")


def aaa(func):
    def bbb():
        print("in bbb")
        func()
    return bbb

# decorated by aaa
@aaa
def ccc():
    print("in ccc")

ccc()

print("####### test decorator #########")


def aaaa(func):
    def bbbb():
        result = func()
        print("in bbbb")
        return result
    return bbbb

# decorated by aaaa
@aaaa
def cccc():
    print("in cccc")

cccc()

print("####### test arguman #########")


def e(func):
    def f(*args):
        print("in e")
        print(*args)
    return f


@e
def g(*args):
    print("in d")

g([1, 2, 3], "a")

print("####### test two decorators #########")


def ee(func):
    @wraps(func)
    def ff(*args):
        print("in ee")
        print(*args)
        func(*args)              # the second decorator wont be called if we dont call func
    return ff


def hh(func):
    @wraps(func)
    def ii(*args):
        print("in hh")
        print(*args)
    return ii


@ee
@hh
def gg(*args):
    print("in gg")

gg([1, 2, 3], "a")



