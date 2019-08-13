import abc

__author__ = 'R.Azh'

# A way of passing a request between a chain of objects
# Avoid coupling the sender of a request to its receiver by giving more than one object a chance to handle the request.
# Chain the receiving objects and pass the request along the chain until an object handles it.


# Handler: defines an interface for handling the requests
# (optional) implements the successor link
class Approver:
    _successor = None

    def set_successor(self, successor):
        self._successor = successor

    @abc.abstractmethod
    def process_request(self, purchase):
        ''' process request '''


# ConcreteHandler: handles requests it is responsible for
# can access its successor
# if the ConcreteHandler can handle the request, it does so; otherwise it forwards the request to its successor
class Director(Approver):
    def process_request(self, purchase):
        if purchase.amount < 10000:
            print("{} approved request# {}".format(type(self).__name__, purchase.number))
        elif self._successor is not None:
            self._successor.process_request(purchase)


class VicePresident(Approver):
    def process_request(self, purchase):
        if purchase.amount < 25000:
            print("{} approved request# {}".format(type(self).__name__, purchase.number))
        elif self._successor is not None:
            self._successor.process_request(purchase)


class President(Approver):
    def process_request(self, purchase):
        if purchase.amount < 100000:
            print("{} approved request# {}".format(type(self).__name__, purchase.number))
        else:
            print("Request# {} requires an executive meeting!".format(purchase.number))


# Class holding request details
class Purchase:
    _number = None
    _amount = None
    _purpose = None

    def __init__(self, number, amount, purpose):
        self._number = number
        self._amount = amount
        self._purpose = purpose

    @property
    def number(self):
        return self._number

    @number.setter
    def number(self, value):
        self._number = value

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, value):
        self._amount = value

    @property
    def purpose(self):
        return self._purpose

    @purpose.setter
    def purpose(self, value):
        self._purpose = value


# Client: initiates the request to a ConcreteHandler object on the chain

larry = Director()
sam = VicePresident()
tammy = President()

larry.set_successor(sam)
sam.set_successor(tammy)

p = Purchase(2034, 350.00, "Assets")
larry.process_request(p)

p = Purchase(2035, 32590.10, "Project X")
larry.process_request(p)

p = Purchase(2036, 122100.00, "Project Y")
larry.process_request(p)