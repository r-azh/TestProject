import abc


class Expression:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def reduce(self, bank, to: str):
        pass


class Money(Expression):
    _amount = 0
    _currency = None

    def __init__(self, amount: int, currency: str):
        self._amount = amount
        self._currency = currency

    def __eq__(self, other):
        return other._amount == self._amount and \
               other.currency == self.currency

    @property
    def amount(self):
        return self._amount

    @abc.abstractmethod
    def times(self, multiplier: int):
        return Money(self._amount * multiplier, self.currency)

    @staticmethod
    def dollar(amount):         # factory method
        return Money(amount, 'USD')

    @staticmethod
    def franc(amount):          # factory method
        return Money(amount, 'CHF')

    @property
    def currency(self):
        return self._currency

    def __repr__(self):
        return f'{self._amount} {self._currency} {self.__class__.__name__}'

    def plus(self, addend) -> Expression:
        return Sum(self, addend)

    def reduce(self, bank, to):
        rate = bank.rate(self.currency, to)
        return Money(self.amount / rate, to)


class Pair:
    from_ = ''
    to = ''

    def __init__(self, from_, to):
        self.from_ = from_
        self.to = to
    # Because we are using  Pair s as keys, we have to implement  equals() and  hashCode() . I'm not going to write
    # tests for these, because we are writing this code in the context of a refactoring. If we get to the payoff of the
    # refactoring and all of the tests run, then we expect the code to have been exercised. If I were programming with
    # someone who didn't see exactly where we were going with this, or if the logic became the least bit # complex, I
    # would begin writing separate tests.

    def __eq__(self, other):
        return self.from_ == other.from_ and self.to == other.to

    def __hash__(self):
        return 0


class Bank:
    rates = dict()

    def reduce(self, source: Expression, to: str) -> Money:
        return source.reduce(self, to)

    def rate(self, from_: str, to: str) -> int:
        # return 2 if from_ == 'CHF' and to == 'USD' else 1
        # To get rid of data duplication for rate, we need to keep a table of rates in the  Bank and look up a rate when
        # we need it. We could use a hashtable that maps pairs of currencies to rates.
        if from_ == to:
            return 1
        return self.rates[Pair(from_, to)]

    def add_rate(self, from_: str, to: str, rate: int):
        self.rates[Pair(from_, to)] = rate


class Sum(Expression):
    augend = 0
    addend = 0

    def __init__(self, augend, addend):
        self.augend = augend
        self.addend = addend

    def reduce(self, bank:Bank, to: str) -> Money:
        amount = self.augend.amount + self.addend.amount
        return Money(amount, to)

