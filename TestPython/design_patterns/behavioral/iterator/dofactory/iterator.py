import abc

__author__ = 'R.Azh'

# Provide a way to access the elements of an aggregate object sequentially without exposing its underlying
# representation.


# Iterator: defines an interface for accessing and traversing elements.
class IAbstractIterator:
    current_item = None
    is_done = None

    @abc.abstractmethod
    def first(self):
        ''' return: an Item '''

    @abc.abstractmethod
    def next(self):
        ''' return: an Item '''


# ConcreteIterator: implements the Iterator interface.
# keeps track of the current position in the traversal of the aggregate.
class Iterator(IAbstractIterator):
    _collection = None
    _current = None
    _step = None

    def __init__(self, collection):
        self._collection = collection
        self._current = 0
        self._step = 1

    def first(self):
        self._current = 0
        return self._collection[self._current]

    def next(self):
        self._current += self._step
        if not self.is_done:
            return self._collection[self._current]
        else:
            return None

    @property
    def step(self):
        return self._step

    @step.setter
    def step(self, value):
        self._step = value

    @property
    def current_item(self):
        return Item(self._collection[self._current])

    @property
    def is_done(self):
        return self._current >= len(self._collection)


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
        return Iterator(self)

    @property
    def count(self):                # as in dofactory but standard way in python is implementing __len__
        return len(self._item)

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

iterator.step = 2
print("Iterating over collection:")
l = [iterator.first()]
while not iterator.is_done:
    l.append(iterator.next())

for i in l[:-1]:          # the last item is None
    print(i.name)