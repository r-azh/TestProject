__author__ = 'R.Azh'

# https://docs.scipy.org/doc/numpy-dev/user/quickstart.html

# SciPy offers a magnitude of algorithms working on arrays
# it is a good habit to always inspect the scipy module before you start implementing a numerical algorithm.

import scipy, numpy

print(scipy.__version__)

# the complete namespace of NumPy is also accessible via SciPy. So, we can use NumPy's machinery via the SciPy
# namespace.

print(scipy.dot is numpy.dot)