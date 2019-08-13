# Aggregate: defines an interface for creating an Iterator object
class IAbstractCollection:
    def create_iterator(self):
        raise NotImplementedError


# ConcreteAggregate: implements the Iterator creation interface to return an instance of the proper ConcreteIterator
class Collection(IAbstractCollection):
    _item = None

    def __init__(self):
        self._item = []

    def create_iterator(self):
        return iter(self)

    def __len__(self):
        return len(self._item)

    def __getitem__(self, i):
        return self._item[i]

    def __setitem__(self, i, value):
        self._item.insert(i, value)


# other classes
class Item:
    _name = None

    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name


# usage
collection = Collection()
collection[0] = Item("Item 0")
collection[1] = Item("Item 1")
collection[2] = Item("Item 2")
collection[3] = Item("Item 3")
collection[4] = Item("Item 4")
collection[5] = Item("Item 5")
collection[6] = Item("Item 6")
collection[7] = Item("Item 7")
collection[8] = Item("Item 8")

iterator = collection.create_iterator()

print("Iterating over collection:")

from itertools import islice

for i in islice(iterator, 0, None, 2):
    print(i.name)

print("iterator will be empty in next use:")
for i in iterator:
    print(i.name)


#  Iterators can only be exhausted (by something
#  like making a list out of them) once. The purpose of this is to save memory by only generating the elements of the
#  iterator as you need them, rather than putting it all into memory at once. If you want to reuse yourobject,
#  just create a list out of it, and then duplicate the list
