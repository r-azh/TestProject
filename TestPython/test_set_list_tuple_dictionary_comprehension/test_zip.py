__author__ = 'R.Azh'

# Another collection that can be iterated over is a zip. A zip is constructed from other
# collections all of the same length. Each element of the zip is a tuple consisting of one
# element from each of the input collections.
# Make an iterator that aggregates elements from each of the iterables.
# Returns an iterator of tuples

print(zip([1, 3, 5], [2, 4, 6]))
print(list(zip([1, 3, 5], [2, 4, 6])))

characters = ['Neo', 'Morpheus', 'Trinity']
actors = ['Keanu', 'Laurence', 'Carrie-Anne']
print(set(zip(characters, actors)))

s = [character+' is played by '+actor for (character, actor) in zip(characters, actors)]
print(s)


x = [1, 2, 3]
y = [4, 5, 6]

x2, y2 = zip(*zip(x, y))
print(x2)
print(y2)
