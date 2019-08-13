__author__ = 'R.Azh'

# The doctest module is easier to use than the unittest, though the later is more suitable for more complex tests.
# The help text of the module is parsed for example python sessions. These examples are run and the results are
# compared against the expected value.
import doctest


def fib(n):
    """
    Calculates the n-th Fibonacci number iteratively

    >>> fib(0)
    0
    >>> fib(1)
    1
    >>> fib(10)
    55
    >>> fib(15)
    610
    >>>

    """
    a, b = 0, 1
    for i in range(n):
        a, b = b, a + b
    return a

if __name__ == "__main__":
    doctest.testmod()
