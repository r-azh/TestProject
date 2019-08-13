import numpy

numpy.set_printoptions(precision=20)    # default is 8
x = numpy.array([2.48E-324])
print(x)

print('#### underflow for 2.47E-324 #### ')
x = numpy.array([2.47E-324])
print(x)


x = 0.00001
y = x ** 64
print(y)

print('#### underflow #### ')
y = x ** 65
print(y)

import sys
print(sys.float_info)

# To mitigate this, one could switch to math libraries such as  mpmath ( http://code.google.com/p/mpmath/ )
# that allow for arbitrary accuracy. However, they are not fast enough to work as a NumPy replacement.
