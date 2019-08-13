import json
import os
from textwrap import TextWrapper

from html2text import HTML2Text

# variable = ''' '''

# print(variable.replace('\"', '\'').encode(encoding='utf-8'))
# print(variable)

html_to_text = HTML2Text()
# result = html_to_text.drop_white_space(variable)
# print(result)

# lines = lines.split()


for file in os.listdir('input'):
    print(file)
    file = 'input/' + file
    lines = ''
    with open(file, "r+") as file:
        lines = file.read()
        # title = html_to_text.handle_tlines)
        # print(lines.split('\n')[6])
        lines = ''.join(lines)
        # print(lines)
        # print(json.dumps(lines))
        # lines = lines.replace("\\", "/\\")
        # lines = lines.replace('\"', '\'')
        # lines = lines.replace('\'', '\\\'')
        lines = lines.replace('\"', '\\\"')
        lines = lines.replace("\n", '')
        lines = lines.replace("\t", '')
        print(lines)
        print()
    with open("new_html.html", "w+") as file2:
        file2.write(lines)


