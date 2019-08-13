__author__ = 'R.Azh'

import os
import tempfile

print('######################  risky methods ############################')
# This will most certainly put you at risk
tmp = os.path.join(tempfile.gettempdir(), 'test_temp.txt')
print(tempfile.gettempdir())
if not os.path.exists(tmp):
    with open(tmp, "w") as file:
        file.write("defaults")

# this is also insecure
f = open(tempfile.mktemp(), "w")
print(f.name)

# this is also insecure : easily predictable.
filename = "{}/{}.tmp".format(tempfile.gettempdir(), os.getpid())
open(filename, "w")
print(filename)

print('######################  safe methods ############################')
# Use the TemporaryFile context manager for easy clean-up
with tempfile.TemporaryFile() as tmp:
    print(tmp.name)
    tmp.write(b'stuff')
    tmp.seek(0)
    x = tmp.read()

# Clean up a NamedTemporaryFile on your own
# delete=True means the file will be deleted on close
tmp = tempfile.NamedTemporaryFile(delete=True)
try:
    print(tmp.name)
    tmp.write(b'stuff')
    print('content: ', tmp.read())
finally:
    tmp.close()     # deletes the file


# Handle opening the file yourself. This makes clean-up
# more complex as you must watch out for exceptions
fd, path = tempfile.mkstemp()
try:
    with os.fdopen(fd, 'w') as tmp:
        print(path)
        print(tmp.name)
        tmp.write('stuff')
finally:
    os.remove(path)


print('######################## temp directory ############################')
# We can also safely create a temporary directory and create temporary files inside it.
# We need to set the umask before creating the file to ensure the permissions on the file only
# allow the creator read and write access.

tmpdir = tempfile.mkdtemp()
predictable_filename = 'myfile'

# Ensure the file is read/write by the creator only
saved_mask = os.umask(0o77)

path = os.path.join(tmpdir, predictable_filename)
print(path)
try:
    with open(path, 'w') as tmp:
        tmp.write('secrets!')
except IOError as e:
    print('IOError')
else:
    os.remove(path)
finally:
    os.umask(saved_mask)
    os.rmdir(tmpdir)
