import math

__author__ = 'R.Azh'

#  Class methods are methods that are not bound to an object, but to… a class!


# class methods are mostly useful for two types of methods:
# Factory methods, that are used to create an instance for a class using for example some sort of pre-processing.
# If we use a @staticmethod instead, we would have to hardcode the Pizza class name in our function, making any class
#  inheriting from Pizza unable to use our factory for its own use.
class Pizza(object):
    def __init__(self, ingredients):
        self.ingredients = ingredients

    @classmethod
    def from_fridge(cls, fridge):
        return cls(fridge.get_cheese() + fridge.get_vegetables())


# Static methods calling static methods: if you split a static methods in several static methods, you shouldn't
# hard-code the class name but use class methods. Using this way to declare ou method, the Pizza name is never directly
#  referenced and inheritance and method overriding will work flawlessly
class Pizza(object):
    def __init__(self, radius, height):
        self.radius = radius
        self.height = height

    @staticmethod
    def compute_area(radius):
        return math.pi * (radius ** 2)

    @classmethod
    def compute_volume(cls, height, radius):
        return height * cls.compute_area(radius)

    def get_volume(self):
        return self.compute_volume(self.height, self.radius)