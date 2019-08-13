import abc


class Expression:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def reduce(self, bank, to: str):
        pass

    @abc.abstractmethod
    def plus(self, addend):
        pass

    @abc.abstractmethod
    def times(self, multiplier: int):
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
    def times(self, multiplier: int) -> Expression:
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

    def plus(self, addend: Expression) -> Expression:
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

    def __eq__(self, other):
        return self.from_ == other.from_ and self.to == other.to

    def __hash__(self):
        return 0


class Bank:
    rates = dict()

    def reduce(self, source: Expression, to: str) -> Money:
        return source.reduce(self, to)

    def rate(self, from_: str, to: str) -> int:
        if from_ == to:
            return 1
        return self.rates[Pair(from_, to)]

    def add_rate(self, from_: str, to: str, rate: int):
        self.rates[Pair(from_, to)] = rate


class Sum(Expression):
    augend = 0
    addend = 0

    def __init__(self, augend: Expression, addend: Expression):
        self.augend = augend
        self.addend = addend

    def reduce(self, bank: Bank, to: str) -> Money:
        amount = self.augend.reduce(bank, to).amount + self.addend.reduce(bank, to).amount
        return Money(amount, to)

    def plus(self, addend: Expression) -> Expression:
        return Sum(self, addend)    # using self works because Sum is Expression

    def times(self, multiplier: int) -> Expression:
        return Sum(self.augend.times(multiplier), self.addend.times(multiplier))

