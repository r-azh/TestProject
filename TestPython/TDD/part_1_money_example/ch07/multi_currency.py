
class Money:
    _amount = 0

    def __eq__(self, other):
        return other._amount == self._amount and \
               type(other).__name__ == type(self).__name__


class Dollar(Money):
    def __init__(self, amount: int):
        self._amount = amount

    def times(self, multiplier: int):
        return Dollar(self._amount * multiplier)


class Franc(Money):
    def __init__(self, amount: int):
        self._amount = amount

    def times(self, multiplier: int):
        return Franc(self._amount * multiplier)
