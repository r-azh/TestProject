__author__ = 'R.Azh'

# Printing first 10 fibonacci numbers, iterative
print("############## iterative #################")

def fibonacci_1(n, first=0, second=1):
    while n != 0:
        print(first, end="\n")  # side-effect
        n, first, second = n-1, second, first + second  # assignment

fibonacci_1(10)

# Printing first 10 fibonacci numbers, functional expression style
print("############## functional expression #################")


fibonacci_a = (lambda n, first=0, second=1:
               " " if n == 0 else
               str(first) + "\n" + fibonacci_a(n-1, second, first+second))
print(fibonacci_a(10))

# Printing a list with first 10 fibonacci numbers, with generators
print("############## generators #################")


def fibonacci_2(n, first=0, second=1):
    while n != 0:
        yield first
        n, first, second = n-1, second, first + second  # assignment

print(list(fibonacci_2(10)))

# Printing a list with first 10 fibonacci numbers, functional expression style
print("############## functional expression #################")

fibonacci_b = (lambda n, first=0, second=1:
               [] if n == 0 else
               [first] + fibonacci_b(n-1, second, first+second))
print(list(fibonacci_b(10)))