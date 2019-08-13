import abc


class Money(abc.ABC):
    _amount = 0
    _currency = None

    def __init__(self, amount: int, currency: str):
        self._amount = amount
        self._currency = currency

    def __eq__(self, other):
        return other._amount == self._amount and \
               type(other).__name__ == type(self).__name__

    @abc.abstractmethod
    def times(self, multiplier: int):
        pass

    @staticmethod
    def dollar(amount):         # factory method
        return Dollar(amount, 'USD')

    @staticmethod
    def franc(amount):          # factory method
        return Franc(amount, 'CHF')

    def currency(self):
        return self._currency


class Dollar(Money):
    def __init__(self, amount, currency):
        super().__init__(amount, currency)

    def times(self, multiplier: int) -> Money:
        return Money.dollar(self._amount * multiplier)


class Franc(Money):
    def times(self, multiplier: int) -> Money:
        return Money.franc(self._amount * multiplier)

