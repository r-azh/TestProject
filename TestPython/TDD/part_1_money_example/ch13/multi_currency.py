import abc


class Expression:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def reduce(self, to: str):
        pass


class Money(Expression):
    _amount = 0
    _currency = None

    def __init__(self, amount: int, currency: str):
        self._amount = amount
        self._currency = currency

    def __eq__(self, other):
        return other._amount == self._amount and \
               other.currency() == self.currency()

    @property
    def amount(self):
        return self._amount

    @abc.abstractmethod
    def times(self, multiplier: int):
        return Money(self._amount * multiplier, self._currency)

    @staticmethod
    def dollar(amount):         # factory method
        return Money(amount, 'USD')

    @staticmethod
    def franc(amount):          # factory method
        return Money(amount, 'CHF')

    def currency(self):
        return self._currency

    def __repr__(self):
        return f'{self._amount} {self._currency} {self.__class__.__name__}'

    def plus(self, addend) -> Expression:
        return Sum(self, addend)

    def reduce(self, to):
        return self


class Bank:
    def reduce(self, source: Expression, to: str) -> Money:
        return source.reduce(to)
        #     Introduced polymorphism to eliminate explicit class checking


class Sum(Expression):
    augend = 0
    addend = 0

    def __init__(self, augend, addend):
        self.augend = augend
        self.addend = addend

    def reduce(self, to: str) -> Money:
        amount = self.augend.amount + self.addend.amount
        return Money(amount, to)


#  Any time we are checking classes explicitly, we should be using polymorphism instead. Because  Sum implements
#  reduce(String) , if  Money implemented it, too, we could then add it to the  Expression interface.
# I'm not entirely happy with the name of the method being the same in  Expression and in  Bank , but having different
#  parameter types in each.
