import re
import string

exception_list = ['(', ')', '*', '+', '.', '?', '[', '\\']
for mark in [c for c in string.punctuation if c not in exception_list]:
    text = mark
    pattern = mark
    print(pattern, ' :: ', text)
    result = re.match(pattern, text)
    print(result)

print('----------------------- after using escape ------------------------------')

for mark in string.punctuation:
    text = mark
    pattern = re.escape(mark)
    print(pattern, ' :: ', text)
    result = re.match(pattern, text)
    print(result)

print('------------------------')

regex_special_characters = ['[', '\\', '^', '$', '.', '|', '?', '*', '+', '(', ')']
# regex_special_characters = "[\^$.|?*+()"
for mark in regex_special_characters:
    text = mark
    pattern = re.escape(mark)
    print(pattern, ' :: ', text)
    result = re.match(pattern, text)
    print(result)
