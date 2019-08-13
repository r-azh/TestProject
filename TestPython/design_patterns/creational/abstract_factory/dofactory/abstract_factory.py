__author__ = 'R.Azh'

# creates an instance of several families of classes:
#   Provide an interface for creating families of related or dependent objects without
#   specifying their concrete classes.


# AbstractFactory: declares an interface for operations that create abstract products
class ContinentFactory:
    def create_herbivore(self):
        pass

    def create_carnivore(self):
        pass


# ConcreteFactory: implements the operations to create concrete product objects
class AfricaFactory(ContinentFactory):
    def create_herbivore(self):
        return WildBeast()

    def create_carnivore(self):
        return Lion()


# ConcreteFactory
class AmericaFactory(ContinentFactory):
    def create_herbivore(self):
        return Bison()

    def create_carnivore(self):
        return Wolf()


# AbstractProduct: declares an interface for a type of product object
class Carnivore:
    def eat(self):
        pass


# AbstractProduct
class Herbivore:
    pass


# Product: defines a product object to be created by the corresponding concrete factory
# implements the AbstractProduct interface
class WildBeast(Herbivore):
    pass


# Product
class Lion(Carnivore):
    def eat(self, herbivore):
        print(type(self).__name__, " eats ", type(herbivore).__name__)


# Product
class Bison(Herbivore):
    pass


# Product
class Wolf(Carnivore):
    def eat(self, herbivore):
        print(type(self).__name__, " eats ", type(herbivore).__name__)


# Client: uses interfaces declared by AbstractFactory and AbstractProduct classes
class AnimalWorld:
    herbivore = None
    carnivore = None

    def __init__(self, factory):
        self.herbivore = factory.create_herbivore()
        self.carnivore = factory.create_carnivore()

    def run_food_chain(self):
        self.carnivore.eat(self.herbivore)


######### usage ###########

africa = AfricaFactory()
animal_world = AnimalWorld(africa)
animal_world.run_food_chain()

america = AmericaFactory()
animal_world = AnimalWorld(america)
animal_world.run_food_chain()