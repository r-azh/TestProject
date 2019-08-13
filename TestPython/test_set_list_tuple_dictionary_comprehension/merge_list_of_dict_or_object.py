from pprint import pprint
# from bson.objectid import ObjectId
import itertools

__author__ = 'R.Azh'

print('################ merged lists of dicts to unique values ######################')

from collections import defaultdict

l1 = [{"index": 1, "b": 2}, {"index": 2, "b": 3}, {"index": 3, "green": "eggs"}]
l2 = [{"index": 1, "c": 4}, {"index": 2, "c": 5}]

d = defaultdict(dict)
# d = {}
for l in (l1, l2):
    for elem in l:
        d[elem['index']].update(elem)
unique_list = d.values()
print('#1 unique_list:', unique_list)

# or for keeping one value other than index

unique_list = {x['index']: x for x in l1 + l2}.values()
print('#2 unique_list:', unique_list)

# or for keeping each unique dict

unique_list = [next(g) for k, g in itertools.groupby(l1 + l2, lambda x: x['index'])]
print('#3 unique_list:', unique_list)

# or for keeping each unique dict

unique_list = l1 + [x for x in l2 if x not in l1]
print('#4 unique_list:', unique_list)


print('\n################## merge multiple dict into one with list values ###############')
dicts = l1 + l2
print(dicts)
super_dict = {}
for d in dicts:
    for k, v in d.items():
        super_dict.setdefault(k, []).append(v)

print('#1 merged_dict:', super_dict)

import collections
super_dict = collections.defaultdict(list)
for d in dicts:
    for k, v in d.items():
        super_dict[k].append(v)
print('#2 merged_dict:', super_dict)

import collections
super_dict = collections.defaultdict(set)
for d in dicts:
    for k, v in d.items():
        super_dict[k].add(v)
print('#3 merged_dict:', super_dict)

print('\n################## merge multiple dict of dict into one with list of values ###############')
dicts = [{'att1': {"index": 1, "b": 2}, 'att2': {"index2": 2, "c": "c"}, 'att3': 'xx'},
      {'att1': {"index": 1, "b": 2}, 'att2': {"index2": 2, "c": "c"}, 'att3': 'xxx'},
      {'att1': {"index": 2, "b": 3}, 'att2': {"index2": 3, "d": "d"}, 'att3': 'yy'},
      {'att1': {"index": 2, "b": 3}, 'att2': {"index2": 3, "d": "d"}, 'att3': 'yyy'},
      {'att1': {"index": 3, "green": "eggs"}, 'att2': {"index2": 3, "d": "d"}, 'att3': 'zzz'},
      {'att1': {"index": 3, "green": "eggs"}, 'att2': {"index2": 3, "d": "d"}, 'att3': 'zzz'}]
print(dicts)

super_dict = {}
for d in dicts:
    for k, v in d.items():
        super_dict.setdefault(k, []).append(v)
print('all unique values: ')
pprint(super_dict)
unique_list = [next(g) for k, g in itertools.groupby(dicts, lambda x: x['att1'])]
# merged_list = [itertools.groupby(dicts, lambda x: x['att1'])]
pprint(unique_list)

# pprint(merged_list)


print('\n################ merged lists of objects to unique values ######################')


class obj:
    _id = None
    name = None

    def __init__(self, name):
        self._id = ObjectId()
        self.name = name

x = obj('X')
y = obj('Y')
z = obj('Z')
d = obj('D')
d._id = x._id

l1 = [x, y]
l2 = [y, z]
l3 = [x, y, d]

t = itertools.groupby(l1 + l2, lambda x: x._id)
unique_list = [next(g) for k, g in itertools.groupby(l1 + l2, lambda x: x._id)]
not_unique_list = [next(g) for k, g in itertools.groupby(l1 + l3, lambda x: x._id)]
unique_list_2 = [k for k, g in itertools.groupby(l1 + l3, lambda x: x._id)]

print(unique_list)
print([i.name for i in unique_list])
print([i.name for i in not_unique_list])
print(unique_list_2)

unique_list = l1 + [x for x in l3 if x not in l1]
print([i.name for i in unique_list])

print(list(set(l1 + l3)))


# works
list_full = l1 + l2 + l3
print([i.name for i in list_full])

print([i.name for i in list_full])

list_full = sorted(list_full, key=lambda a: a._id)
unique_list = []
for key, g in itertools.groupby(list_full, key=lambda x: x._id):       #it wont work if list_full is not sorted
    g_list = list(g)
    print()
    print(key, ' : ', g_list, [i.name for i in g_list])
    unique_list.append(g_list[0])
    # g_list_2 = {k: v for k, v in x.__dict__ for x in g_list}  # because id is a dict wont work
    # print(g_list_2)
print(unique_list)
print([i.name for i in unique_list])

print('\n################ merge objects with different attributes ######################')
# nobj.__dict__ = oobj.__dict__.copy()
# destination.__dict__.update(source.__dict__)



