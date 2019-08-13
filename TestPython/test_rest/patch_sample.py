from re import split


def apply_path_operations_on_data(data, operations):
    for operation in operations:
        value = operation.get('value')
        paths = split(operation['path'], '.')
        key = paths[-1]
        _data = data
        for path in paths[:-1]:
            _data = _data[path]
        op = operation.get('op')
        if op == 'remove':
            try:
                _data[key].remove(int(value))
            except:
                pass
        elif op == 'add':
            _data[key].add(int(value))
        else:
            _data[key] = set(value) if type(value) == list and type(_data[key]) == set else value

    return data

body = [
    {
        "op": "set",
        "path": "role",
        "value": 123
    },
    {
        "op": "set",
        "path": "status",
        "value": True,
    },
    {
        "op": "set",
        "path": "inboxes",
        "value": []
    }
]

apply_path_operations_on_data(body, 'add')