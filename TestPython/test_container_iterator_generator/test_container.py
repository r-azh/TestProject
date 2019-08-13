__author__ = 'R.Azh'

# Containers are data structures holding elements, and that support membership tests.
# They are data structures that live in memory, and typically hold all their values
#  in memory, too. In Python, some well known examples are:
#
# list, deque, …
# set, frozensets, …
# dict, defaultdict, OrderedDict, Counter, …
# tuple, namedtuple, …
# str

# Technically, an object is a container when it can be asked whether it contains a certain element.

assert 1 in [1, 2, 3]   # lists
assert 4 not in [1, 2, 3]

assert 1 in {1, 2, 3}   # set
assert 4 not in {1, 2, 3}

assert 1 in (1, 2, 3)      # tuples
assert 4 not in (1, 2, 3)

d = {1: 'foo', 2: 'bar', 3: 'qux'}  # dictionary: will check the keys
assert 1 in d
assert 4 not in d
assert 'foo' not in d  # 'foo' is not a _key_ in the dict

s = 'foobar'    # string: if it "contains" a substring
assert 'b' in s
assert 'x' not in s
assert 'foo' in s  # a string "contains" all its substrings


# Even though most containers provide a way to produce every element they contain, that
# ability does not make them a container but an iterable.

# Not all containers are necessarily iterable. An example of this is a Bloom filter
