import math

__author__ = 'R.Azh'


def get_primes(number):
    while True:
        if is_prime(number):
            print("\n", number)
            yield number
        number += 1


def is_prime(number):
    if number > 1:
        if number == 2:
            return True
        if number % 2 == 0:
            return False
        for current in range(3, int(math.sqrt(number) + 1), 2):
            if number % current == 0:
                return False
        return True
    return False


def solve_number_10():
    total = 2
    for next_prime in get_primes(3):
        if next_prime < 200000:
            print(" : ", total)
            total += next_prime
        else:
            print(total)
            return

solve_number_10()

print('########################################')

# other = yield foo means, "yield foo and, when a value is sent to me, set other to that value."
# You can "send" values to a generator using the generator's send method.
# In this way, we can set number to a different value each time the generator yields
# When you're using send to "start" a generator, you must send None.


def get_primes2(number):
    while True:
        if is_prime(number):
            number = yield number
        number += 1


def print_successive_primes(iterations, base=10):
    prime_generator = get_primes2(base)
    prime_generator.send(None)
    for power in range(iterations):
        print(prime_generator.send(base ** power))

print_successive_primes(10)