__author__ = 'R.Azh'

# Provide a unified interface to a set of interfaces in a subsystem. Façade defines a higher-level interface
# that makes the subsystem easier to use.

# Subsystem classes: implement subsystem functionality.
# handle work assigned by the Facade object.
# have no knowledge of the facade and keep no reference to it.

class Bank:
    def has_sufficient_savings(self, customer, amount):
        print("check bank for ", customer.name, " for amount ", amount)
        return True


class Credit:
    def has_good_credit(self, customer):
        print("check credit for ", customer.name)
        return True


class Loan:
    def has_no_bad_loans(self, customer):
        print("check loans for ", customer.name)
        return True


# customer class
class Customer:
    _name = None

    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name


# Facade: knows which subsystem classes are responsible for a request.
# delegates client requests to appropriate subsystem objects.
class Mortgage:
    _bank = None
    _credit = None
    _loan = None

    def __init__(self):
        self._bank = Bank()
        self._credit = Credit()
        self._loan = Loan()

    def is_eligible(self, customer, amount):
        print("{} applies for {} loan\n".format(customer.name, amount))
        eligible = True
        if not self._bank.has_sufficient_savings(customer, amount):
            eligible = False
        elif not self._loan.has_no_bad_loans(customer):
            eligible = False
        elif not self._credit.has_good_credit(customer):
            eligible = False
        return eligible

# usage
mortgage = Mortgage()
customer = Customer("Ann McKinsey")
eligible = mortgage.is_eligible(customer, 125000)

print("\n{} has been {}".format(customer.name, ("Approved" if eligible else "Rejected")))

