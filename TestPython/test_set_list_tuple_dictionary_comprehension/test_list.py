__author__ = 'R.Azh'

# Python represents sequences of values using lists. In a list, order is significant and repeated
# elements are allowed.
# A list can contain a set or another list. However, a set cannot contain a list since lists are mutable.
li = [1, 9, 8, 4]
li2 = [elem*2 for elem in li]
print(li2)
print(len(li))

print(sum(li))
print(sum([1, 1, 0, 1, 0, 1, 0], -9))


# List concatenation
print([1, 2, 3]+["my", "word"])
li2 = sum([[1, 2, 3], [4, 5, 6], [7, 8, 9]], [])
print(li2)

print('\n##################### list comprehension #######################')
li2 = [2*x for x in {2, 1, 3, 4, 5}]
print(li2)

li2 = [2*x for x in [2, 1, 3, 4, 5]]
print(li2)

li2 = [x*y for x in [1, 2, 3] for y in [10, 20, 30]]
print(li2)

li2 = [x*y for x in {1, 2, 3} for y in {10, 20, 30}]
print(li2)

print('\n##################### list elelment #######################')
print(['in', 'the', 'CIT'][1])


my_list = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90]
print("slice: ", my_list[1:3])  # slice

print("prefix: ", my_list[:5])   # prefix

print("suffix: ", my_list[5:])  # suffix

# You can use a colon-separated triple a:b:c if you want the slice to include every cth element
print("slices that skip: ", my_list[1::2])     # slices that skip
print(my_list[::2])

[x, y, z] = [2*x for x in {2, 1, 3}]    # unpacking
print(x, ", ", y, ", ", z)

list_of_lists = [[1, 1], [2, 4], [3, 9]]
print([y for [x, y] in list_of_lists])

my_list[2] = "-"
print(my_list)

print('\n##################### filtering lists #########################')

# [mapping-expression for element in source-list if filter-expression]
li = ["a", "mpilgrim", "foo", "b", "c", "b", "d", "d"]
print([elem for elem in li if len(elem) > 1])
print([elem for elem in li if elem != "b"])
print([elem for elem in li if li.count(elem) == 1])

a = [1, 2, 3]
print(a)
b = [4, 5, 6]
print(b)
a.extend(b)
print("extend:", a)
a.append(7)
print("append:", a)
print("inline append return:", a.append(8))

li = []
if li:
    print("list is not none")

print("############### convert to list ################")
print(list(range(10)))
print(list((1, 2, 3)))
print(list({10, 9, 8}))


print('############### reversed ########################')
l = [x*x for x in reversed([4, 5, 10])]
print(l)

print('############### any, all ########################')
li = ["a", "bar", "foo", "b", "c", "b", "d", "d"]
a = ['a', 'b', 'c']
if any(x in li for x in a):
    print(True)

if all(x in li for x in a):
    print(True)

print(a.index('b'))
a.insert(1, 'zz')
print(a)

b = a.remove('b')
print(a)

del a[1]
print(a)

print('################ split list ######################')
mylist = range(30)
goodvals = [1, 3, 7, 11, 13, 17, 19, 23, 29]
good, bad = [], []
for x in mylist:
    (bad, good)[x in goodvals].append(x)
print(mylist)
print(good)
print(bad)

bad.reverse()
print(bad)

print('################ concat lists ######################')
listone = [1, 2, 3]
listtwo = [4, 5, 6]
joined_list = listone + listtwo
print(joined_list)

# or

import itertools
joined_list = [item for item in itertools.chain(listone, listtwo)]
print(joined_list)

print('################ merged lists to unique values ######################')
l1 = [1, 2, 3, 4, 5]
l2 = [4, 5, 6, 7, 8]
mergedlist = list(set(l1 + l2))
print(mergedlist)







