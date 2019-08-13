__author__ = 'R.Azh'

print('Python provides some simple data structures for grouping together multiple values, '
      '\nand integrates them with the rest of the language. These data structures are called collections')

# A set is an unordered collection in which each value occurs at most once

s = {1+2, 3, 'a', 'a'}
print(s)

# The cardinality of a set S is the number of elements in the set.
print(len(s))

# The empty set is represented by set()
my_set = set()
print(my_set)

# You cannot make a set that has a set as element.
# a set cannot contain a list since lists are mutable.
print("sum: ", sum({1, 2, 3}))
print(sum({1, 2, 3}, 10))

print(3 in s)
print('a' not in s)

print('\n############ union, intersection ##########')
print({1, 2, 3} | {2, 3, 4, 5})    # union
s.union({2, 3, 4, 5})
print(s)

print({1, 2, 3} & {2, 3, 4, 5})    # intersection
s.intersection({3, 'a'})
print(s)

# A value that can be altered is a mutable value. Sets are mutable;
# elements can be added and removed using the add and remove methods

s.add('b')
print(s)
s.remove(3)
print(s)

# add to a set all the elements of another collection (e.g. a set or a list)
s.update({'010', '020', '030'})
print(s)

# intersect a set with another collection, removing from the set all elements not in the other collection
s.intersection_update({'010', 'hello', '040', 'a'})
print(s)

print('\n#########################  copy refrence ##########################')
t = s
t.update({'hello', 'world', 'of', 'python'})
print(t)
print(s)

print('\n######################### copy value ##############################')
q = s.copy()
q.intersection_update({'010', 'a'})
print(q)
print(s)

print('\n######################### set comprehension ########################')

s2 = {2*x for x in {1, 2, 3}}
print(s2)

s3 = {x*x for x in s2 | {3, 5}}
print(s3)

s4 = {x*x for x in s2 | {3, 5} if x > 3}
print(s4)

s5 = {x*y for x in {1, 2, 3} for y in {3, 2, 1}} # {1, 2, 3, 2, 4, 6, 3, 6, 9}
# iterates over the Cartesian product of two sets
print(s5)

s6 = {x*y for x in {1, 2, 3} for y in {2, 3, 4} if x != y}
print(s6)

print("############### convert to set ################")
print(set(range(10)))
print(set((1, 2, 3)))
print(set([10, 9, 8]))