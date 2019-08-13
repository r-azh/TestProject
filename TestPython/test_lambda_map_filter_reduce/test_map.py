__author__ = 'R.Azh'

# the advantage of the lambda operator can be seen when it is used in combination with the map() function.
# map() is a function which takes two arguments:
# r = map(func, seq)
# func is the name of a function and
#  the second a sequence (e.g. a list) seq.
# map() applies the function func to all the elements of the sequence seq.
# With Python 3, map() returns an iterator.
# Guido van Rossum, the author of the Python, gives his reasons for dropping lambda, map(), filter() and reduce().

def fahrenheit(T):
    return (float(9)/5)*T + 32


def celsius(T):
    return (float(5)/9)*(T-32)

temperatures = (36.5, 37, 37.5, 38, 39)
print(temperatures)
F = map(fahrenheit, temperatures)
C = map(celsius, F)

temperatures_in_Fahrenheit = list(map(fahrenheit, temperatures))
print(temperatures_in_Fahrenheit)
temperatures_in_Celsius = list(map(celsius, temperatures_in_Fahrenheit))
print(temperatures_in_Celsius)

print('\n############## using lambda ####################')

d = [39.2, 36.5, 37.3, 38, 37.8]
print(d)
F = list(map(lambda x: (float(9)/5)*x + 32, d))
print(F)
C = list(map(lambda x: (float(5)/9)*(x-32), F))
print(C)

# map() can be applied to more than one list. The lists have to have the same length.
a = [1, 2, 3, 4]
b = [17, 12, 11, 10]
c = [-1, -4, 5, 9]

print(list(map(lambda x, y: x+y, a, b)))

print(list(map(lambda x, y, z: 2.5*x + 2*y - z, a, b, c)))

print("\n############ important: ##########################")


def square(x):
    return x*x

squares = map(square, [1, 2, 3])
print("returns list:", list(squares))
print("returns empty list:", list(squares))
# The crux is that the return value of map in Python 3 (and imap in Python 2) is not a list - it's an iterator!
# The elements are consumed when you iterate over an iterator unlike when you iterate over a list.
# When dealing with iterators you have to remember that they are stateful and that they mutate as you traverse them.
# Lists are more predictable since they only change when you explicitly mutate them; they are containers.