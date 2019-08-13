import timeit
__author__ = 'R.Azh'

normal_py_sec = timeit.timeit('sum(x*x for x in range(1000))',
                              number=10000)
naive_np_sec = timeit.timeit(
    'sum(na*na)',
    setup="import numpy as np; na=np.arange(1000)",
    number=10000)
good_np_sec = timeit.timeit(
    'na.dot(na)',
    setup="import numpy as np; na=np.arange(1000)",
    number=10000)
print("Normal Python: %f sec" % normal_py_sec)
print("Naive NumPy: %f sec" % naive_np_sec)         # 3.5 times longer
print("Good NumPy: %f sec" % good_np_sec)       # 25 times faster


# in every algorithm we are about to implement, we should always
# look how we can move loops over individual elements from Python to some of the
# highly optimized NumPy or SciPy extension functions.

