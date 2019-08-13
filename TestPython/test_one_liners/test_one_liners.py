from functools import reduce

__author__ = 'R.Azh'
print('--------------------------------------------------------------------------------------')
print('########## Function that returns the set of all subsets of its argument ###########\n')

s = [10, 9, 1, 10, 9, 1, 1, 1, 10, 9, 7]
print(s)
f = lambda x: [[y for j, y in enumerate(set(x)) if (i >> j) & 1] for i in range(2**len(set(x)))]

print(f(s))

g = lambda l: reduce(lambda z, x: z + [y + [x] for y in z], l, [[]])
print(g(s))

print('--------------------------------------------------------------------------------------')
print('########## Function that returns the set of all subsets of its argument ###########\n')

