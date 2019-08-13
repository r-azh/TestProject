__author__ = 'R.Azh'

r = '/\*.*\*/'  # for comment

exp = '/\*([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*\*+/'   # for comment
# http://www.regexr.com/


print(ord('۰'))  # returns character code
print(ord('۹'))
print(ord('ی'))
print(ord('ي'))

import string

punc = string.punctuation


print(string.punctuation)
import re


punc = '\\' + '\\'.join(punc)
pat_fa = '^[' + punc + '0-9 \u0622-\u06CC' + ']+$'  # fa - persian digit excluded
pat_fa = '^[' + punc + '\u06F0-\u06F9 \u0622-\u06CC' + ']+$'  # fa - persian digit included
# or
# farsi_alef_char = chr(1570)
# farsi_ye_char = chr(1740)
# farsi_0_char = chr(1776)
# farsi_9_char = chr(1785)
# punc = string.punctuation
# pat_fa = '^[{} {}-{} {}-{} \n]+$'.format(punc, farsi_0_char, farsi_9_char, farsi_alef_char,
#                                                       farsi_ye_char)
pat_en = '^[' + punc + '0-9 a-zA-Z' + ']+$'  # fa

print(pat_fa)
print(pat_en)

r = re.match(pat_fa, 'بسم الله الرحمن الرحیم {۸۶۸}')
print(r)

r = re.match(pat_en, 'In the name of GOD! My age is! ۸۶۸')
print(r)

r = r'/domians/(?P<domain_id>)/users/(?P<user_id>)/teams/(?P<team_id>)/'
text = 'http://localhost/domains/1/users/1/teams/1/members'

r_ = re.compile(r)
result = re.search(r, text)
print(result)

match = r_.match(text)
print(match)
