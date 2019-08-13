__author__ = 'R.Azh'

#  tuples have no methods
# Like a list, a tuple is an ordered sequence of elements.
#  However, tuples are immutable so they can be elements of sets.
t = (1, 1+1, 3)
print(t)

print("############## indexing #####################")
t = ("a", "b", "mpilgrim", "z", "example")
print(t)
print(t[0])
print(t[-1])
print(t[1:3])
print((1, {"A", "B"}, 3.14)[2])

print("############## unpacking #####################")
(a, b) = (1, 5-3)
print(a)

a, b = (1, 5-3)
print(a)

a, b = 1, 5-3
print(a)

c = [y for (x, y) in [(1, 'A'), (2, 'B'), (3, 'C')]]
print(c)

print("############### convert to tuple ################")
print(tuple(range(10)))
print(tuple([1, 2, 3]))
print(tuple({10, 9, 8}))
print(len(tuple(range(5))))

print("###############################################")
isin = "z" in t
print(isin)

first_name = "rezvan"
last_name = "azh"
key = '%s_%s'%(first_name, last_name)
print(key)

salaries = {}
salaries[('John', 'Smith')] = 10000.0
salaries[('John', 'Parker')] = 99999.0
print(salaries[('John', 'Smith')])

print(1, 1)

v = {'network_element': ('a', 5),
     'site': ('b', 4),
     'exchange': ('c', 3),
     'city': ('d', 2),
     'province': ('e', 1)}


l = [x for (x, y) in v.values() if y < 3]
d = {k: x for k, (x, y) in v.items() if y < 3}
print(d)
print(l)

print('##################################################')
t = tuple('(a,b)')
print(t)