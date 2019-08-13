class Dollar:
    _amount = 0

    def __init__(self, amount: int):
        self._amount = amount

    def times(self, multiplier: int):
        return Dollar(self._amount * multiplier)

    def __eq__(self, other):
        return other._amount == self._amount


#  Remember, our cycle has different
# phases (they go by quickly, often in seconds, but they are phases.):
# 1. Write a test.
# 2. Make it compile.
# 3. Run it to see that it fails.
# 4. Make it run.
# 5. Remove duplication.
# The different phases have different purposes. They call for different styles of solution, different aesthetic
# viewpoints. The first three phases need to go by quickly, so we get to a known state with the new functionality. We
# can commit any number of sins to get there, because speed trumps design, just for that brief moment.
# Now I'm worried. I've given you a license to abandon all the principles of good design. Off you go to your
# teams—"Kent says all that design stuff doesn't matter." Halt. The cycle is not complete. A four-legged Aeron chair
# falls over. The first four steps of the cycle won't work without the fifth.
# Good design at good times. Make it run, make it right.
# There, I feel better. Now I'm sure you won't show anyone except your partner your code until you've removed the
# duplication. Where were we? Ah, yes. Violating all the tenets of good design in the interest of speed (penance for
#  our sin will occupy the next several chapters).

class Franc:
    _amount = 0

    def __init__(self, amount: int):
        self._amount = amount

    def times(self, multiplier: int):
        return Franc(self._amount * multiplier)

    def __eq__(self, other):
        return other._amount == self._amount
