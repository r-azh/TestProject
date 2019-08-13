import os

__author__ = 'R.Azh'

from os.path import dirname, abspath, splitext, split

print(abspath(__file__))
print(dirname(abspath(__file__)))
dd = dirname(dirname(abspath(__file__)))
print(dd)

# or path = '../../../filename'

print('\n', dirname(__file__))
this_directory = splitext(dirname(__file__))[0]
upward_directory = split(dirname(this_directory))[1]

print(this_directory)
print(upward_directory)

# getcwd() returns current working directory of a process
print(os.getcwd())

# Change the current working directory to path.
os.chdir('/var')
print(os.getcwd())


print(os.curdir)