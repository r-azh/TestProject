__author__ = 'R.Azh'

import numpy as np
from numpy import *


version = np.__version__
print(version)

a = np.array([0, 1, 2, 3, 4, 5])
print(a)


dimention = a.ndim
print(dimention)

element_count = a.shape
print(element_count)

b = a.reshape((3, 2))
print(b)
print(b.ndim)

print('############# copy by reference #############')

b[1][0] = 77
print(b)
print(a)

print('################# true copy ###################')
c = a.reshape((3, 2)).copy()
c[0][0] = -99
print(c)
print(a)

print('################# operations ###################')
# operations are propagated to the individual elements
# conditions are also propagated to individual elements

print(a * 2)
print(a ** 2)
print(a > 4)

# but in python
l = [1, 2, 3, 4, 5]
print(l*2)  # duplicates the list
# print(l ** 2) # won't work

print('################# indexing ###################')
# can use arrays as indexes
print(a)
b = a[np.array([2, 3, 4])]
print(b)

d = a[a > 4]
print(d)

print('################# trim outliers ###################')
# this can be used to trim outliers
b = a.copy()
b[b > 4] = 4
print(b)

c = a.copy()
c[0] = -2
print(c)
print(c.clip(0, 4))

print('################# Handling nonexisting values ###################')
c = np.array([1, 2, np.NAN, 3, 4])
print(c)
print(np.isnan(c))
d = c[~np.isnan(c)]
print(d)
print(np.mean(d))

print('################# array data type ###################')
# NumPy arrays always have only one data type.
print(a)
print('type: ', a.dtype)

# If we try to use elements of different types, such as the ones shown in the following
# code, NumPy will do its best to coerce them to be the most reasonable common
# data type
e = np.array([1, "stringy"])
print('\n', e)
print('type: ', e.dtype)

f = np.array([1, "stringy", set([1, 2, 3])])
print('\n', f)
print('type: ', f.dtype)



