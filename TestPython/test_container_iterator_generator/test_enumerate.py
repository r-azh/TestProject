data = ['foo', 'bar', 'baz']

for index, item in enumerate(data):
    print(index, item)

print('-------')
for index, item in enumerate(data, 1):  # starting index from
    print(index, item)