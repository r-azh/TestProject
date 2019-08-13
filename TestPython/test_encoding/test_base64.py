import base64

__author__ = 'R.Azh'


file_content = open('logo-small.png', 'rb').read()
encoded_string = base64.b64encode(file_content)
print(file_content)
print(encoded_string)


encoded_string = base64.b64encode(open('logo-small.png', 'rb').read())
print(encoded_string)