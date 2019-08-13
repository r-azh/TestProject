class Dollar:
    _amount = 0

    def __init__(self, amount: int):
        self._amount = amount

    def times(self, multiplier: int):
        return Dollar(self._amount * multiplier)

    def __eq__(self, other):
        return other._amount == self._amount
