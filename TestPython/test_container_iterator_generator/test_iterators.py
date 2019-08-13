__author__ = 'R.Azh'
# an iterator is a stateful helper object that will produce the next value when you call next() on it.
#  Any object that has a __next__() method is therefore an iterator. How it produces a value is irrelevant.

# So an iterator is a value factory. Each time you ask it for "the next" value,
# it knows how to compute it because it holds internal state.

# All of the itertools functions return iterators.


from itertools import count

counter = count(start=13)   # produce infinite sequence
print(next(counter))
print(next(counter))
print(next(counter))

#####################################
print('############################')

from itertools import cycle
colors = cycle(['red', 'white', 'blue'])    # produce infinite sequences from finite sequences
print(next(colors))
print(next(colors))
print(next(colors))
print(next(colors))

#####################################
print('############################')

from itertools import islice    # produce finite sequences from infinite sequences
colors = cycle(['red', 'white', 'blue'])  # infinite
limited = islice(colors, 0, 4)            # finite
for x in limited:                         # so safe to use for-loop on
    print(x)

