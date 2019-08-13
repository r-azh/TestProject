import abc

__author__ = 'R.Azh'


# This particular way of implementing abstract method has a drawback. If you write a class that inherits from Pizza
# and forget to implement get_radius, the error will only be raised when you'll try to use that method.
class Pizza(object):
    def get_radius(self):
        raise NotImplementedError


# here's a way to triggers this way earlier, when the object is being instantiated, using the abc module that's
# provided with Python.
class BasePizza(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def get_radius(self):
         """Method that should do something."""

    @abc.abstractmethod
    def get_ingredients(self):
         """Returns the ingredient list."""

# Using abc and its special class, as soon as you'll try to instantiate BasePizza or any class inheriting from it,
#  you'll get a TypeError.
b = BasePizza()


# Keep in mind that declaring a method as being abstract, doesn't freeze the prototype of that method. That means
# that it must be implemented, but i can be implemented with any argument list.
class Calzone(BasePizza):
    def get_ingredients(self, with_egg=False):
        egg = Egg() if with_egg else None
        return self.ingredients + egg


# That means that we could also implement it as being a class or a static method
class DietPizza(BasePizza):
    @staticmethod
    def get_ingredients():
        return None


# Starting with Python3 it's  possible to use the @staticmethod and @classmethod decorators on top of @abstractmethod
class BasePizza(object):
    __metaclass__  = abc.ABCMeta

    ingredient = ['cheese']

    @classmethod
    @abc.abstractmethod
    def get_ingredients(cls):
         """Returns the ingredient list."""
         return cls.ingredients
# if you think this going to force your subclasses to implement get_ingredients as a class method, you are wrong.
# This simply implies that your implementation of get_ingredients in the BasePizza class is a class method


# In Python, contrary to methods in Java interfaces, you can have code in your abstract methods and call it via super()
class BasePizza(object):
    __metaclass__  = abc.ABCMeta

    default_ingredients = ['cheese']

    @classmethod
    @abc.abstractmethod
    def get_ingredients(cls):
         """Returns the ingredient list."""
         return cls.default_ingredients


class DietPizza(BasePizza):
    def get_ingredients(self):
        return ['egg'] + super(DietPizza, self).get_ingredients()