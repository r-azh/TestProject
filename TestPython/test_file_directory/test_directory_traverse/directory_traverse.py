__author__ = 'R.Azh'
import os

# http://www.bogotobogo.com/

# get the home directory
home = os.path.expanduser("~")
print(home)

# This will ensure it works on all platforms.
from os.path import expanduser

home = expanduser("~")
print(home)

print('\n########################## split the path #############################\n')
# Both os.path.basename() and os.path.dirname() functions use the os.path.split(path) function to split the
# pathname path into a pair; (head, tail).

path = '/foo/bar/item'
print('path: ', path)
head = os.path.dirname(path)
print('head:', head)
tail = os.path.basename(path)
print('tail:', tail)

path2 = '/foo/bar/item/'
print('path: ', path2)
head = os.path.dirname(path2)
print('head:', head)
tail = os.path.basename(path2)
print('tail:', tail)

split = os.path.split(path)
print('split: ', split)
split = os.path.split(path2)
print('split: ', split)

print('\n############################ os.walk() ######################################\n')

# The os.walk() generate the file names in a directory tree by walking the tree either top-down or bottom-up.
# For each directory in the tree rooted at directory top, it yields a 3-tuple: (dirpath, dirnames, filenames)
# dirpath: a string for the path to the directory.
# dirnames: a list of the names of the subdirectories in dirpath (excluding '.' and '..').
# filenames: a list of the names of the non-directory files in dirpath.
# Note that the names in the lists contain no path components. To get a full path (which begins with top) to a file
# or directory in dirpath, do os.path.join(dirpath, name).

# path = '.'
# path = '..'
path = '/home/azh/Documents/ebook'

print('\ndir_paths:')
for dirpath, dirname, filename in os.walk(path):
    print(dirpath)

print('\ndir_names:')
for dirpath, dirname, filename in os.walk(path):
    print(dirname)

print('\nfile_names:')
for dirpath, dirname, filename in os.walk(path):
    print(filename)

print('\n**********************************\n')
for dirpath, dirs, files in os.walk(path):
    path = dirpath.split('/')
    print('|', (len(path)) * '---', '[', os.path.basename(dirpath), ']')
    for f in files:
        print('|', len(path) * '---', f)

print('\n ########################## recursively traverse directories and files 1 #################\n')

# 1
# for dir_path, dir_names, file_names in os.walk('.'):
#     for file_name in file_names:
#         f_name = os.path.join(dir_path, file_name)
#         with open(f_name) as myfile:
#             print(myfile.read())

print('\n ########################## recursively traverse directories and files 2 #################\n')
# 2
# find files which have more than one import.
# print(" import count :")
# for dirpath, dirs, files in os.walk("..."):
#     for filename in files:
#         fname = os.path.join(dirpath, filename)
#         if fname.endswith('.py'):
#             with open(fname) as myfile:
#                 line = myfile.read()
#                 c = line.count('import')
#                 if c > 1:
#                     print(fname, c)


# dangerous
# os.removedirs(name)
# Remove directories recursively. Works like rmdir() except that, if the leaf directory is successfully removed,
#  removedirs() tries to successively remove every parent directory mentioned in path until an error is raised (which
#  is ignored, because it generally means that a parent directory is not empty). For example,
#  os.removedirs('foo/bar/baz') will first remove the directory 'foo/bar/baz', and then remove 'foo/bar' and 'foo' if
#  they are empty. Raises OSError if the leaf directory could not be successfully removed.
