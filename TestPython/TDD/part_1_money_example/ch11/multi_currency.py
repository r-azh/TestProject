import abc


class Money:
    _amount = 0
    _currency = None

    def __init__(self, amount: int, currency: str):
        self._amount = amount
        self._currency = currency

    def __eq__(self, other):
        return other._amount == self._amount and \
               other.currency() == self.currency()

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
