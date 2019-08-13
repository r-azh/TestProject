from functools import reduce

__author__ = 'R.Azh'


# functional techniques: composition, pipelining, higher order functions.
# Functional code is characterised by one thing: the absence of side effects.

print("#\n###### Don’t iterate over lists. Use map and reduce. #######\n#")
# not functional
import random

names = ['Mary', 'Isla', 'Sam']
code_names = ['Mr. Pink', 'Mr. Orange', 'Mr. Blonde']

for i in range(len(names)):
    names[i] = random.choice(code_names)

print(names)

# functional
print("############## functional #################")


secret_names = map(lambda x: random.choice(['Mr. Pink',
                                            'Mr. Orange',
                                            'Mr. Blonde']),
                   names)
print(list(secret_names))

# not functional
print("############## not functional #################")

sentences = ['Mary read a story to Sam and Isla.',
             'Isla cuddled Sam.',
             'Sam chortled.']

sam_count = 0
for sentence in sentences:
    sam_count += sentence.count('Sam')

print(sam_count)

# functional
print("############### functional ####################")

sam_count = reduce(lambda a, x: a + x.count('Sam'),
                   sentences,
                   0)
print(sam_count)

# map and reduce have many friends that provide useful, tweaked versions of their basic behaviour.
#  For example: filter, all, any and find.

# not functional
print("############## not functional #################")

people = [{'name': 'Mary', 'height': 160},
          {'name': 'Isla', 'height': 80},
          {'name': 'Sam'}]

height_total = 0
height_count = 0
for person in people:
    if 'height' in person:
        height_total += person['height']
        height_count += 1

if height_count > 0:
    average_height = height_total / height_count

print(average_height)

# functional
print("################# functional ####################")

heights = list(map(lambda x: x['height'],
               filter(lambda x: 'height' in x, people)))
# not using list wont return values returns a map
# and it only can be traveresd once second time it will return []
print("list:", heights)
if len(heights) > 0:
    from operator import add
    average_height = reduce(add, heights) / len(heights)
    print(average_height)
# The elements are consumed when you iterate over an iterator unlike when you iterate over a list.
# When dealing with iterators you have to remember that they are stateful and that they mutate as you traverse them.
# Lists are more predictable since they only change when you explicitly mutate them; they are containers.

