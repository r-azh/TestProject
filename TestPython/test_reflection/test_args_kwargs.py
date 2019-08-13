__author__ = 'R.Azh'


# *args to pass a non-keyworded, variable-length argument list
def test_var_args(*args):
    for arg in args:
        print(arg)

test_var_args(1, "two", 3)

print('\n')


# **kwargs is used to pass a keyworded, variable-length argument list.
def test_var_kwargs(**kwargs):
    for arg in kwargs:
        print(arg)

    print('\n')
    for key in kwargs:
        print('{}: {}'.format(key, kwargs[key]))

test_var_kwargs(farg=1, myarg2="two", myarg3=3)


print('###################### Using *args and **kwargs when calling a function ####################')


def test_var_args_call(arg1, arg2, arg3):
    print('\n arg1: {},\n arg2: {},\n arg3: {} '.format(arg1, arg2, arg3))

args = ('three', 2)
test_var_args_call(1, *args)

kwargs = {"arg3": 3, "arg2": "two"}
test_var_args_call(1, **kwargs)