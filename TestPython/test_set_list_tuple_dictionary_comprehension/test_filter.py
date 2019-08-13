# filter creates a list of elements for which a function returns True.
# it's like a for loop but faster

number_list = range(-5, 5)
less_than_zero = filter(lambda x: x < 0, number_list)
print(list(less_than_zero))
