from copy import copy
from typing import Any


def get_dict_value_from_key_chain(dict_, dot_separated_key_chain, default: Any = Exception):
    keys = dot_separated_key_chain.split('.')

    data = copy(dict_)
    for key in keys:
        if isinstance(data, dict) and key in data:
            data = data[key]
        else:
            if default == Exception:
                raise KeyError(f'rsa_key:"{rsa_key}" is not in "{data}"')
            else:
                return default

    return data

a = {
    'role': 1,
    'inbox_access': {
        'inboxes': 2,
        'dict2': {
            'some_key': 8
        }
    }
}

x = get_dict_value_from_key_chain(a, 'inbox_access.inboxes')
print(x)

x = get_dict_value_from_key_chain(a, 'inbox_access')
print(x)

x = get_dict_value_from_key_chain(a, 'role')
print(x)

x = get_dict_value_from_key_chain(a, 'inbox_access.dict2')
print(x)

x = get_dict_value_from_key_chain(a, 'inbox_access.dict2.some_key')
print(x)

x = get_dict_value_from_key_chain(a, 'inbox_access.inboxes.dict2', default=None)
print(x)

x = get_dict_value_from_key_chain(a, 'inboxes.inbox_access', default=None)
print(x)

x = get_dict_value_from_key_chain(a, 'inboxes.inbox_access')
print(x)


