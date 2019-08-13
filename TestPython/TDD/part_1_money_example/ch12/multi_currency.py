import abc


class Expression:
    __metaclass__ = abc.ABCMeta


class Money(Expression):
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

    def plus(self, addend) -> Expression:
        return Money(self._amount + addend._amount, self._currency)


class Bank:
    def reduce(self, source: Expression, to: str) -> Money:
        return Money.dollar(10)     # data duplication


# The most difficult design constraint is that we want most of the code in the system to be unaware that it potentially
# is dealing with multiple currencies. One possible strategy is to immediately convert all money values into a reference
# currency. However, this doesn't allow exchange rates to vary easily.
# Instead we would like a solution that lets us conveniently represent multiple exchange rates, and still allows most
# arithmetic-like expressions to look like, well, arithmetic.
# Objects to the rescue. When the object we have doesn't behave the way we want it to, we make another object with the
# same external protocol (an imposter) but a different implementation.
# This probably sounds a bit like magic. How do we know to think of creating an imposter here? I won't kid you—there is
# no formula for flashes of design insight. Ward Cunningham came up with the "trick" a decade ago, and I haven't seen it
# independently duplicated yet, so it must be a pretty tricky trick. TDD can't guarantee that we will have flashes of
# insight at the right moment. However, confidence-giving tests and carefully factored code give us preparation for
# insight, and preparation for applying that insight when it comes. p37

# That doesn't seem like enough reasons to tip the scales permanently, but it is enough for me to start in this
# direction. I'm also perfectly willing to move responsibility for reduction to  Expression if it turns out that
#  Bank s don't need to be involved.
