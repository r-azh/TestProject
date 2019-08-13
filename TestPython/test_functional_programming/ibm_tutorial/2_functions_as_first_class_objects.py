__author__ = 'R.Azh'

# The main thing we do with our first class objects, is pass them to our FP built-in
# functions map(), reduce(), and filter(). Each of these functions accepts a function object as its first argument.
# map() performs the passed function on each corresponding item in the specified list(s), and returns a list of results.
# reduce() performs the passed function on each subsequent item and an internal accumulator of a final result; for
# example, reduce(lambda n,m:n*m, range(1,10)) means "factorial of 10" (in other words, multiply each item by the
# product of previous multiplications).
# filter() uses the passed function to "evaluate" each item in a list, and return a winnowed list of the items
# that pass the function test.
from functools import reduce

print(reduce(lambda n, m: n * m, range(1, 10)))

