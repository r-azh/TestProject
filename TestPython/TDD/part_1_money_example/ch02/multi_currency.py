class Dollar:
    _amount = 0

    def __init__(self, amount: int):
        self._amount = amount

    def times(self, multiplier: int):
        # return None # to fail test and add the following fix
        return Dollar(self._amount * multiplier)

    @property
    def amount(self):
        return self._amount
