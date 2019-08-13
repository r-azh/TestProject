from functools import reduce
from itertools import chain

__author__ = 'R.Azh'

# A very large percentage of program errors—and the problem that drives programmers to debuggers—occur because
# variables obtain unexpected values during the course of program execution. Functional programs bypass this
# particular issue by simply not assigning values to variables at all.


# print out a list of pairs of numbers whose product is more than 25
print('############ Imperative Python code for "print big products" ############')
xs = (1, 2, 3, 4)
ys = (10, 15, 3, 22)
bigmuls = []
for x in xs:
    for y in ys:
        if x*y > 25:
            bigmuls.append((x, y))
print(bigmuls)

print('############ Functional approach ############')

bigmuls = lambda xs, ys: filter(lambda x, y: x * y > 25, combine(xs, ys))
combine = lambda xs, ys: map(None, xs*len(ys), dupelms(ys, len(xs)))
dupelms = lambda lst, n: reduce(lambda s, t: s + t, map(lambda l, n = n: [l]*n, lst))
print(bigmuls((1, 2, 3, 4), (10, 15, 3, 22))) # ?
# for e in bigmuls(xs, ys):
#     print(e)

# combine : produces a list of all pairs of elements from two input lists
print(combine(xs, ys))

print('############ best approach ############')

# Rather than either the imperative or functional examples given, the best (and functional) technique is:
print([(x, y) for x in (1, 2, 3, 4) for y in (10, 15, 3, 22) if x*y > 25])