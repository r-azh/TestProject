import abc

__author__ = 'R.Azh'
# A fine-grained instance used for efficient sharing
# Use sharing to support large numbers of fine-grained objects efficiently.

# in this example a relatively small number of Character objects is shared many times by a document that has
# potentially many characters.


# Flyweight: declares an interface through which flyweights can receive and act on extrinsic state.
class Character:
    symbol = None
    width = None
    height = None
    ascent = None
    descent = None
    point_size = None

    @abc.abstractmethod
    def display(self, point_size):
        "abstract method"


# ConcreteFlyweight: implements the Flyweight interface and adds storage for intrinsic state, if any.
# A ConcreteFlyweight object must be sharable. Any state it stores must be intrinsic, that is,
# it must be independent of the ConcreteFlyweight object's context.
class CharacterA(Character):
    def __init__(self):
        self.symbol = 'A'
        self.height = 100
        self.width = 120
        self.ascent = 70
        self.descent = 0

    def display(self, point_size):
        self.point_size = point_size
        print(self.symbol, "(pointsize {})".format(self.point_size))


class CharacterB(Character):
    def __init__(self):
        self.symbol = 'B'
        self.height = 100
        self.width = 140
        self.ascent = 72
        self.descent = 0

    def display(self, point_size):
        self.point_size = point_size
        print(self.symbol, "(pointsize {})".format(self.point_size))


class CharacterZ(Character):
    def __init__(self):
        self.symbol = 'A'
        self.height = 100
        self.width = 100
        self.ascent = 68
        self.descent = 0

    def display(self, point_size):
        self.point_size = point_size
        print(self.symbol, "(pointsize {})".format(self.point_size))


# UnsharedConcreteFlyweight: not all Flyweight subclasses need to be shared. The Flyweight interface enables sharing,
# but it doesn't enforce it. It is common for UnsharedConcreteFlyweight objects to have ConcreteFlyweight objects as
# children at some level in the flyweight object structure (as the Row and Column classes have).


# FlyweightFactory: creates and manages flyweight objects
# ensures that flyweight are shared properly. When a client requests a flyweight, the FlyweightFactory objects assets
# an existing instance or creates one, if none exists.
class CharacterFactory:
    _characters = None

    def __init__(self):
        self._characters = {}

    def get_character(self, key):
        character = None
        if key in self._characters:
            character = self._characters[key]
        else:
            if key == 'A':
                character = CharacterA()
            elif key == 'B':
                character = CharacterB()
            elif key == 'Z':
                character = CharacterZ()
            self._characters[key] = character
        return character


# Client: maintains a reference to flyweight(s).
# computes or stores the extrinsic state of flyweight(s).
document = "AAZZBBZB"
factory = CharacterFactory()

poin_size = 10

for c in document:
    poin_size += 1
    character = factory.get_character(c)
    character.display(poin_size)
