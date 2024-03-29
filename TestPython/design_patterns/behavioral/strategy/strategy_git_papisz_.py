
#!/usr/bin/python
# -*- coding: utf-8 -*-

"""The Strategy Pattern Example."""


class Knight(object):

    """Represents our knight."""

    def __init__(self, age, name, gender):
        self.age = age
        self.name = name
        self.gender = gender

    def __repr__(self):
        return "Name: {}, Age: {}, Gender: {}".format(self.name, self.age, self.gender)


def old_knights_validator(knight):
    """Validate if the knight is old."""
    return knight.age > 60


def female_knights_validator(knight):
    """Validate if the knight is a female."""
    return knight.gender == 'F'


class Arena(object):

    """A gathering of knights based on validator."""

    validator = None

    def __init__(self, name, validator):
        self.name = name
        self.validator = validator
        self.knights = []

    def add_knight(self, knight):
        """Add a knight if he or she validates."""
        if self.validator(knight):
            self.knights.append(knight)

    def __repr__(self):
        return '{} Arena\n======\n'.format(self.name) + ''.join(['Knight: {}\n'.format(knight) for knight in self.knights])

# usage
if __name__ == "__main__":
    # Creating some knights...
    anne = Knight(62, "Anne", 'F')
    lancelot = Knight(72, "Lancelot", 'M')
    joan = Knight(19, "Joan of Arc", 'F')
    galahad = Knight(30, "Galahad", 'M')

    # Creating arenas...
    ladies_arena = Arena("Ladies", female_knights_validator)
    elders_arena = Arena("The Elders", old_knights_validator)

    # Knights enter the arenas!
    ladies_arena.add_knight(anne)
    ladies_arena.add_knight(lancelot)
    ladies_arena.add_knight(joan)
    ladies_arena.add_knight(galahad)

    elders_arena.add_knight(anne)
    elders_arena.add_knight(lancelot)
    elders_arena.add_knight(joan)
    elders_arena.add_knight(galahad)

    print(ladies_arena)
    print(elders_arena)