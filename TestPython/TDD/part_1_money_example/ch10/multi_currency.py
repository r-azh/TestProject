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
        return Dollar(amount, 'USD')

    @staticmethod
    def franc(amount):          # factory method
        return Franc(amount, 'CHF')

    def currency(self):
        return self._currency

    def __repr__(self):
        return f'{self._amount} {self._currency} {self.__class__.__name__}'


class Dollar(Money):
    def __init__(self, amount, currency):
        super().__init__(amount, currency)


class Franc(Money):
    pass


# We already have a red bar, and we'd prefer not to write a test when we have a red bar.
# We'd prefer not to write a test when we have a red bar. But we are about to change real model code, and we can't
# change model code without a test. The conservative course is to back out the change that caused the red bar so we're
# back to green. Then we can change the test for equals(), fix the implementation, and retry the original change.
