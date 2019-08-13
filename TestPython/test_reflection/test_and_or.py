__author__ = 'R.Azh'

#  0, '', [], (), {}, and None are false in a boolean context; everything else is true
# By default, instances of classes are true in a boolean context, but you can define special methods
# in your class to make an instance evaluate to false
# If all values are true in a boolean context, "and" returns the last value.
# If any value is false in a boolean context, "and" returns the first false value

print('a' and 'b')
print('' and 'b')
print('a' and 'b' and 'c')

# If any value is true, "or" returns that value immediately
# If all values are false, "or" returns the last value
# "or" evaluates values only until it finds one that is true in a boolean context, and then it ignores the rest.
# This distinction is important if some values can have side effects.

print('a' or 'b')
print('' or 'b')
print('' or [] or {})

def sidefx():
    print("in sidefx")
    return 1

print('a' or sidefx())

# similar to bool ? a : b in C
# but If the value of a is false, the expression will not work as you would expect it to.
#  (Can you tell I was bitten by this? More than once?)
a = "first"
b = "second"
print(1 and a or b)
print(0 and a or b)

a = ""
print(1 and a or b)

# The real trick behind the and-or trick, is to make sure that the value of a is never false.
# One common way of doing this is to turn a into [a] and b into [b],
# then taking the first element of the returned list, which will be either a or b.
print((1 and [a] or [b])[0])
# Since [a] is a non-empty list, it is never false