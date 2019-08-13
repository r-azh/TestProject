__author__ = 'R.Azh'

import ipdb


ipdb.set_trace()
ipdb.set_trace(context=5)  # will show five lines of code
                           # instead of the default three lines
ipdb.pm()
ipdb.run('x[0] = 3')
# result = ipdb.runcall(function, arg0, arg1, kwarg='foo')
result = ipdb.runeval('f(1,2) - 3')


# python -m ipdb mymodule.py


# You can also enclose code with the with statement to launch ipdb if an exception is raised:

from ipdb import launch_ipdb_on_exception

with launch_ipdb_on_exception():
    print('hi'),
    x, y = 1, 0
    if 1 == (x/y):
        print('hello')



# in any function you want to debug add
# import ipdb; ipdb.set_trace()
# when django gets there it will go into debug mode.