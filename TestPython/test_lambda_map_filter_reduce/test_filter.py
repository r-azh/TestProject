__author__ = 'R.Azh'

# filter(function, sequence)
# offers an elegant way to filter out all the elements of a sequence "sequence",
#  for which the function function returns True.

fibonacci = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
print(fibonacci)
odd_numbers = list(filter(lambda x: x % 2, fibonacci))
print(odd_numbers)
even_numbers = list(filter(lambda x: x % 2 == 0, fibonacci))
print(even_numbers)
even_numbers = list(filter(lambda x: x % 2 - 1, fibonacci))
print(even_numbers)
