# map applies a function to all the items in an input_list
# map(function_to_apply, list_of_inputs)

items = [1, 2, 3, 4, 5]
squared = map(lambda x: x**2, items)

print(list(squared))


def inc(x):
    return x + 1


incremented = map(inc, items)
print(list(incremented))

# instead of list_of_inputs we can even have a list of functions


def multiply(x):
    return x*x


def add(x):
    return x + x


funcs = [multiply, add]

for i in range(5):
    value = map(lambda x: x(i), funcs)
    print(list(value))
