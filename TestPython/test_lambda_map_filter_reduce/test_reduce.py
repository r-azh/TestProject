__author__ = 'R.Azh'
# Guido van Rossum:
# "So now reduce(). This is actually the one I've always hated most, because, apart from a few examples
# involving + or *, almost every time I see a reduce() call with a non-trivial function argument, I need
# to grab pen and paper to diagram what's actually being fed into that function before I understand what
#  the reduce() is supposed to do. So in my mind, the applicability of reduce() is pretty much limited to
#  associative operators, and in all other cases it's better to write out the accumulation loop explicitly."

# reduce(func, seq)
# continually applies the function func() to the sequence seq. It returns a single value.


import functools
print(functools.reduce(lambda x, y: x+y, [47, 11, 42, 13]))

# 47   11   42   13
#   58      42   13
#       100      13
#            113

from functools import reduce

f = lambda a, b: a if (a > b) else b
print(reduce(f, [47, 11, 42, 102, 13]))

g = lambda x, y: x+y
print(reduce(g, range(1, 102)))

print(reduce(lambda x, y: x*y, range(1, 50)))


