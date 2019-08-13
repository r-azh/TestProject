__author__ = 'R.Azh'

# Abstract base classes (ABCs)
# abc makes it possible for abstract class to :
# - instantiating the base class is impossible
# - forgetting to implement interface methods in one of the subclasses raises an error as early as possible.

from abc import ABCMeta, abstractmethod


class Base(metaclass=ABCMeta):
    @abstractmethod
    def foo(self):
        pass

    @abstractmethod
    def bar(self):
        pass


class Concrete(Base):
    def foo(self):
        pass

c = Concrete()