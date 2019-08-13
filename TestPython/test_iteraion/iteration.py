__author__ = 'R.Azh'

# iterate with every item important
# you may not actually need to work with the entire sequence as a whole; you are interested solely
# in each item within it.
last_name = "Smith"
count = 0
for letter in last_name:
    print(letter, " ", count)
    count += 1


print("------------------------")

# just have the list as a whole and get each item where it needed
# Not all sequences need to be loaded in their entirety in advance, and many don’t even need to have a finite
# upper limit at all.
# pure iteration : without the need to populate a list in advance.
count = 0
while count < 5:
    print(last_name[count], " ", count)
    count += 1
