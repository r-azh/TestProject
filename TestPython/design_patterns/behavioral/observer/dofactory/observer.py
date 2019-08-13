__author__ = 'R.Azh'

# Define a one-to-many dependency between objects so that when one object changes state, all its dependents are
# notified and updated automatically.


# Subject: knows its observers. Any number of Observer objects may observe a subject
# provides an interface for attaching and detaching Observer objects.
class Stock:
    _symbol = None
    _price = None
    _investors = None

    def __init__(self, symbol, price):
        self._symbol = symbol
        self._price = price
        self._investors = []

    def attach(self, investor):
        self._investors.append(investor)

    def detach(self, investor):
        self._investors.remove(investor)

    def notify(self):
        for investor in self._investors:
            investor.update(self)
        print("-")

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if self._price != value:
            self._price = value
            self.notify()

    @property
    def symbol(self):
        return self._symbol


# ConcreteSubject: stores state of interest to ConcreteObserver
# sends a notification to its observers when its state changes
class IBM(Stock):
    def __init__(self, symbol, price):
        super().__init__(symbol, price)


# Observer: defines an updating interface for objects that should be notified of changes in a subject.
class IInvestor:

    def update(self, stock):
        raise NotImplementedError


# ConcreteObserver: maintains a reference to a ConcreteSubject object
# stores state that should stay consistent with the subject's
# implements the Observer updating interface to keep its state consistent with the subject's
class Investor(IInvestor):
    _name = None
    _stock = None

    def __init__(self, name):
        self._name = name

    def update(self, stock):
        self._stock = stock
        print("Notified {} of {}'s change to {}".format(self._name, self._stock.symbol, self._stock.price))

    @property
    def stock(self):
        return self._stock

    @stock.setter
    def stock(self, value):
        self._stock = value


# usage
ibm = IBM("IBM", 120.00)
ibm.attach(Investor("Sorros"))
ibm.attach(Investor("Berkshire"))

ibm.price = 120.10
ibm.price = 121.00
ibm.price = 120.50
ibm.price = 120.75
