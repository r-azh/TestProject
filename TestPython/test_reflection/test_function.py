
field_names = {
    'a': 'x',
    'b': 'y'
}


def print_(x=None, y=None):
    print(x, y)

args = {
    field_names['a']: 'hallow'
}

print_(**args)

args2 = {
    True: 'x'
}

print_(ar)