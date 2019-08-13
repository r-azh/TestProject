from enum import Enum


class En(Enum):
    A = {'en': 'hi', 'fa': 'سلام'}
    B = {'en': 'hi1', 'fa': 'سلام1'}



list_all_items = list(map(lambda x:x, En))
print(list_all_items)