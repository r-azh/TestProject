from itertools import islice

__author__ = 'R.Azh'

# this class is both an iterable (because it sports an __iter__() method),
# and its own iterator (because it has a __next__() method)
#  iterator is like a lazy factory

class fib:
    def __init__(self):
        self.prev = 0
        self.curr = 1

    def __iter__(self):
        return self

    def __next__(self):
        value = self.curr
        self.curr += self.prev
        self.prev = value
        return value



f = fib()
print(list(islice(f, 0, 10)))

