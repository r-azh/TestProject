__author__ = 'R.Azh'

# A mutable object can be changed after it's created, and an immutable object can't.
# a mutable data type can have values added, removed, or changed in place.
#  Immutable data types cannot be changed.

# Python imposes the restriction that the elements of a set must not be mutable,
# and sets are mutable. The reason for this restriction will be clear to a student of data
# structures from the error message in the following example:

# {{1, 2}, 3}

# There is a nonmutable version of set called frozenset. Frozensets can be elements of sets.

print('\nLists are mutable and tuples are immutable')
int_list = [4, 9]
int_tuple = (4, 9)

int_list[0] = 1
print(int_list)
# int_tuple[0] = 1  # raises: TypeError: 'tuple' object does not support item assignment

print('\nstrings are immutable in Python')
test_string = 'mutable?'
# test_string[7] = '!'  # TypeError: 'str' object does not support item assignment
# if I need a mutable string to do something like character swapping? Well then use a byte array.

print(" \n\timmutable: Numeric types: int, float, complex, string, tuple, frozen set, bytes")
print(" \n\tmutable: list, dict, set, byte array, classes, class instances")

print("\n########################### memory ################################\n")

container = ["If", "you", "are", "iterating", "a", "lot", "and", "building", "a", "large", "string,", "you", "will",
             "waste", "a", "lot", "of", "memory", "creating", "and", "throwing", "away", "objects"]
string_build = ""
for data in container:
    string_build += str(data)
print(string_build)

# more efficient #cuts down on the total number of objects allocated by almost half.
builder_list = []
for data in container:
    builder_list.append(str(data))
result = " ".join(builder_list)
print(result)

# even better: list comprehension
# which is cleaner code and runs faster
result = " ".join([str(data) for data in container])
print(result)

print("\n######################### some points ###########################")

# because Python only evaluates functions definitions once and a list is a mutable object,
# every call that uses the default list will be using the same list


def my_function(param=[]):
    param.append("thing")
    return param

print(my_function())  # prints: ["thing"]
print(my_function())  # prints: ["thing", "thing"]

# Do not put a mutable object as the default value of a function parameter. Immutable types are perfectly
#  safe. If you want to get the intended effect, do this:


def my_function2(param=None):
    if param is None:
        param = []
    param.append("thing")
    return param

print(my_function2())
print(my_function2())

print("\n######################### changing mutable/immutable objects ###########################")

# x = something # immutable type
# print(x)
# func(x)
# print(x) # prints the same thing
# 
# x = something # mutable type
# print(x)
# func(x)
# print(x) # might print something different
# 
# x = something # immutable type
# y = x
# print(x)
# # some statement that operates on y
# print(x) # prints the same thing
# 
# x = something # mutable type
# y = x
# print(x)
# # some statement that operates on y
# print(x) # might print something different


x = 'foo'
y = x
print(x)    # foo
y += 'bar'
print(x)    # foo

x = [1, 2, 3]
y = x
print(x)    # [1, 2, 3]
y += [3, 2, 1]
print(x)    # [1, 2, 3, 3, 2, 1]


def func(val):
    val += 'bar'

x = 'foo'
print(x)    # foo
func(x)
print(x)    # foo


def func(val):
    val += [3, 2, 1]

x = [1, 2, 3]
print(x)     # [1, 2, 3]
func(x)
print(x)    # [1, 2, 3, 3, 2, 1]
