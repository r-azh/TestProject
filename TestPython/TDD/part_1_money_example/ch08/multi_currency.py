import abc


class Money(abc.ABC):
    _amount = 0

    def __eq__(self, other):
        return other._amount == self._amount and \
               type(other).__name__ == type(self).__name__

    @abc.abstractmethod
    def times(self, multiplier: int):
        pass

    # The next step forward is not obvious. The two subclasses of  Money aren't doing enough work to justify their
    # existence, so we would like to eliminate them. But we can't do it with one big step, because that wouldn't make
    # a very effective demonstration of TDD.
    # we would be one step closer to eliminating the subclasses if there were fewer references to the subclasses
    # directly.
    @staticmethod
    def dollar(amount):
        return Dollar(amount)

    # We are now in a slightly better position than before. No client code knows that there is a subclass called Dollar.
    # By decoupling the tests from the existence of the subclasses, we have given ourselves freedom to change
    # inheritance without affecting any model code.
    # Decoupled test code from the existence of concrete subclasses by introducing factory methods
    @staticmethod
    def franc(amount):
        return Franc(amount)


class Dollar(Money):
    def __init__(self, amount: int):
        self._amount = amount

    def times(self, multiplier: int) -> Money:
        return Dollar(self._amount * multiplier)


class Franc(Money):
    def __init__(self, amount: int):
        self._amount = amount

    def times(self, multiplier: int) -> Money:
        return Franc(self._amount * multiplier)
