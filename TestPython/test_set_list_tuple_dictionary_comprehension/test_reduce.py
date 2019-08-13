# reduce is usefull for performing some computation on a list and return the result

product = 1
num_list = [1, 2, 3, 4]
for num in num_list:
    product = product * num
print(product)

# using reduce above code will be:
from functools import reduce

product = reduce(
    lambda x, y: x * y,
    num_list
)
print(product)