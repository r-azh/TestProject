__author__ = 'R.Azh'

mydict = {"server": "mpilgrim", "database": "master", "uid": "sa", "pwd": "secret"}

print(mydict.keys())
print(mydict.values())
print(mydict.items())

# list comprehensions
print([k for k, v in mydict.items()])
print([v for k, v in mydict.items()])
print(["%s=%s" % (k, v) for k, v in mydict.items()])

print("\n###########################################\n")

dic = {'Neo': 'Philip', 'Agent Smith': 'Hugo', 'Trinity': 'Carrie-Anne', 'Morpheus': 'Laurence'}
d7 = [k + " is played by " + v for (k, v) in dic.items()]
print(d7)
print(d7.pop())
print(d7)

print("\n###########################################\n")

print({0: 'zero', 0: 'nothing'})

print("id" in mydict)
print(mydict['Neo'] if 'Neo' in mydict else 'NOT PRESENT')

mydict["location"] = "US"
print(mydict)

print("############ Dictionary comprehensions ################")
d1 = {k: v for (k, v) in [(3, 2), (4, 0), (100, 1)]}
print(d1)

d2 = {(x, y): x*y for x in [1, 2, 3] for y in [1, 2, 3]}    # tuple as key
print(d2)

d3 = [2*x for x in {4: 'a', 3: 'b'}.keys()]
print(d3)

d4 = [x for x in {4: 'a', 3: 'b'}.values()]
print(d4)

print("############ union/intersection ################")
d5 = [k for k in {'a': 1, 'b': 2}.keys() | {'b': 3, 'c': 4}.keys()]
print(d5)
d6 = [k for k in {'a': 1, 'b': 2}.keys() & {'b': 3, 'c': 4}.keys()]
print(d6)

print('#############################################')
d8 = {k: v for (k, v) in [(3, 2), (4, 0), (100, 1)]}
print(d8)

print('################# deep copy ##############')
from copy import deepcopy

d9 = deepcopy(d8)
print(d9)
if 5 in d9.keys():
    del d9[5]
del d9[4]
print(d9)

# [StateCountDetail.create_from_state_count(i) for i in states if i["state"] not in ["NoShowtime",
#                                                                                                   "NotEnoughShowtime"]]
print('#################  comparing dicts  ##############')
d1 = {'a': 1, 'b': 2, 'c': 3, 'd': {'aa': 11, 'bb': 22}}
d2 = {'a': 1, 'b': 2, 'c': 3, 'd': {'aa': 11, 'bb': 22}}

if d1 == d2:
    print('equal')

l1 = [d1, d2]


print('##########  cant use a dict as key in dict ###########')

# d3 = {k['d']: 0 for k in l}
# print(d3)

# d4 = {}
# d4[{'aaa': 111}] = 111
# print(d4)
d3 = {'a': 1, 'b': 2, 'c': 3, 'd': {'aa': 1, 'bb': 22}}
l2 = [d1, d2, d3]

print('########## merge dicts ###########')

from functools import reduce
from itertools import groupby
from operator import add, itemgetter
#
#
# def merge_records_by(key, combine):
#     """Returns a function that merges two records rec_a and rec_b.
#        The records are assumed to have the same value for rec_a[key]
#        and rec_b[key].  For all other keys, the values are combined
#        using the specified binary operator.
#     """
#     return lambda rec_a, rec_b: {
#         k: rec_a[k] if k == key else combine(rec_a[k], rec_b[k])
#         for k in rec_a
#     }
#
#
# def merge_list_of_records_by(key, combine):
#     """Returns a function that merges a list of records, grouped by
#        the specified key, with values combined using the specified
#        binary operator."""
#     keyprop = itemgetter(key)
#     return lambda lst: [
#         reduce(merge_records_by(key, combine), records)
#         for _, records in groupby(sorted(lst, key=keyprop), keyprop)
#     ]

# merger = merge_list_of_records_by('d', add)
# print(merger(l1 + l2))

result = []
l2 = sorted(l2, key=lambda a: a['d']['aa'])

for key, g in groupby(l2, key=lambda x: x['d']):
    # print(key, 'g: ', list(g))   # consumes g so the next
    www = list(g)
    # result.append({'s': key, 'sum': sum([i['a'] for i in list(g)])})
    result.append({'s': www[0]['d'], 'sum': sum([i['a'] for i in www])})

for r in result:
    print(r)

print('########## remove keys form dict ###########')
print(d3)
d2 = (d3.pop(key) for key in ['d', 'a']) # don't work
# print(d2)
print(d3)

for key in ['d', 'a']:
    del d3[key]
print(d3)

print('########## check if a key exists in dict ###########')
if 'b' in d3:
    print('exists')

if 'c' in d3.keys():
    print('exists')

if d3.get('c'):
    print('exists')

print('########## dict update ################')
di = {'Name': 'Zara', 'Age': 7}
di['family'] = 'aj'
dict2 = {'Sex': 'female'}

di.update(dict2)
print(di)

print()


print('########## Multiple levels of keys as variable ################')


d = {'a': {'b': {'c': 'hi'}}}

import operator
key = {'key1': ['a', 'b', 'c']}

print(reduce(operator.getitem, key['key1'], d))


print('########## find in a list of dict  ################')
a = [
    {'main_color': 'red', 'second_color': 'blue'},
    {'main_color': 'yellow', 'second_color': 'green'},
    {'main_color': 'yellow', 'second_color': 'blue'},
]

if any(d['main_color'] == 'red' for d in a):
    print('exists')

#  or If the key could also be missing the above code can give you a KeyError

if any(d.get('main_color', None) == 'red' for d in a):
    print('exists')


x = next(i for i, d in enumerate(a) if 'main_color' in d)
print(x)

# print index
print(list((i, d) for i, d in enumerate(a)))
x = next(i for i, d in enumerate(a) if d['main_color'] == 'yellow')
print(x)
print(a[x])



