class Dollar:
    _amount = 0

    def __init__(self, amount: int):
        self._amount = amount

    def times(self, multiplier: int):
        # return None # to fail test and add the following fix
        return Dollar(self._amount * multiplier)

    # def equals(self, object_: object) -> bool:
    #     return object_.amount == self.amount

    def __eq__(self, other):
        return other.amount == self.amount

    @property
    def amount(self):
        return self._amount
