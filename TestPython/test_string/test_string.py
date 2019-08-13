__author__ = 'R.Azh'

print('############ path ##############')
import ntpath

print(ntpath.basename("a/b/c"))


def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

print(path_leaf("/e/f/g"))

file_name = "123321.jpg"
splitted_file_name = file_name.rsplit('.', 1)
print(splitted_file_name)

print('\n######### process string ###########')

print(str(None))

s = "this   is\na\ttest"
print(s)
print(s.split())
print(" ".join(s.split()))

# ljust pads the string with spaces to the given length.
# If the given length is smaller than the length of the string, ljust will simply
# return the string unchanged. It never truncates the string.
s2 = " this is another string"
print(s2.ljust(10))

li = ['a', 'b', 'c']
print("\n".join(li))

my_string = "blah, lots  ,  of ,  spaces, here "
s = [x.strip() for x in my_string.split(',')]
print(s)

mylist = my_string.replace(' ', '').split(',')
print(mylist)

result = map(lambda s: s.strip(), my_string.split(','))
print(result)

result = map(str.strip, my_string.split(','))
print(result)


print('\n############# find ###################')

if any(x in s2 for x in li):
    print(True)

if all(x in s2 for x in li):
    print(True)
else:
    print(False)

s3 = "string abc"
if all(x in s3 for x in li):
    print(True)

str1 = "this is string example....wow!!!"
str2 = "exam"
print(str1)
print(str1.find(str2))
print(str1.find(str2, 10))
print(str1.find(str2, 40))
print(str2 in str1)

s3 = s2.rstrip('g')
print(s3)

s4 = s2.strip().lstrip('t')
print(s4)

s5 = ''
if not s5:
    print('check for empty string')

str3 = 'abcD'

if 'A' in str3:
    print(True)
else:
    print(False)

