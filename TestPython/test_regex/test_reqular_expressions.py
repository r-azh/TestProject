import string

__author__ = 'R.Azh'

import re

_string = "  blah, lots  ,  of ,  spaces, here "
pattern = re.compile("^\s+|\s*,\s*|\s+$")
print([x for x in pattern.split(_string) if x])


s = re.sub(r'\s', '', _string).split(',')
print(s)

result = [x for x in re.split(',| ', _string) if x != '']
print(result)

filter(None, re.split('[, ]', _string))

print(string.punctuation)

item_to_validate = '1r'
start_with_letters_string_pattern = '^[a-zA-Z]+[_\-.@ 0-9 a-zA-Z]*$'
if not re.match(start_with_letters_string_pattern, item_to_validate):
    print('dont match')

