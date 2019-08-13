__author__ = 'R.Azh'


class Parent:
    _id = None
    name = None

    def __init__(self, id, name):
        self._id = id
        self.name = name

    def print_content(self):
        print(self._id, self.name, self.family)


class Child(Parent):
    family = None

    def __init__(self, id, name, family):
        super().__init__(id, name)
        self.family = family


child = Child(1, 'rezvan', 'azh')
child.print_content()