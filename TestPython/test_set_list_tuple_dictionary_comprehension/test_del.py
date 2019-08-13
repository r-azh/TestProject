__author__ = 'R.Azh'


# Deletion of a name removes the binding of that name from the local or global namespace
# Assigning None to a name does not remove the binding of the name from the namespace
class Foo:
    pass

foo = Foo()

del foo     # instead of foo = None

print("################### del in lists ######################")
values = [100, 200, 300, 400, 500, 600, 300]
print(values)
del values[1]
print(values)

# Use remove to remove by value. It searches for the first element that has the specified value and removes it.
values.remove(300)
print(values)

del values[1:3]
print(values)


colors = {"red": 100, "blue": 50, "purple": 75}
print(colors)
del colors["red"]
print(colors)

print('\n # pop returns the removed element of the list # ')
x = ['a', 'b', 'c', 'd', 'd', 'd', 'd', 'd', 'e']
print(x.pop(2))

print('\n # del is used to remove an element by index # ')
del x[3]
print(x)

print('\n # remove is used to remove the first matching value in the list # ')
x.remove('d')
print(x)
