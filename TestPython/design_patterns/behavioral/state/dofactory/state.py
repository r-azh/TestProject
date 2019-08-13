__author__ = 'R.Azh'

# Allow an object to alter its behavior when its internal state changes. The object will appear to change its class.


# State: defines an interface for encapsulating the behavior associated with a particular state of the Context.
class State:
    _account = None
    _balance = None
    _interest = None
    _lower_limit = None
    _upper_limit = None

    @property
    def account(self):
        return self._account

    @account.setter
    def account(self, value):
        self._account = value

    @property
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self, value):
        self._balance = value

    def deposit(self, amount):
        raise NotImplementedError

    def withdraw(self, amount):
        raise NotImplementedError

    def pay_interest(self):
        raise NotImplementedError


# Concrete State: each subclass implements a behavior associated with a state of Context
# Red indicates that account is overdrawn
class RedState(State):
    _service_fee = None

    def __init__(self, state):
        self.balance = state.balance
        self.account = state.account
        self._initialize()

    def _initialize(self):
        self._interest = 0.0
        self._lower_limit = -100.0
        self._upper_limit = 0.0
        self._service_fee = 15.00

    def deposit(self, amount):
        self.balance += amount
        self.state_change_check()

    def withdraw(self, amount):
        self.balance -= self._service_fee
        print("No funds available for withdrawal!")

    def pay_interest(self):
        pass

    def state_change_check(self):
        if self.balance > self._upper_limit:
            self.account.state = SilverState(self)


# Silver indicates a non-interest bearing state
class SilverState(object):
    def __init__(self, balance, account):
        self.balance = balance
        self.account = account
        self._initialize()

    @classmethod                    # another constructor with different arguments(standard way: using classmethod)
    def from_state(cls, state):
        return cls.__init__(state.balance, state.account)

    def _initialize(self):
        self._interest = 0.0
        self._lower_limit = 0.0
        self._upper_limit = 1000.0

    def deposit(self, amount):
        self.balance += amount
        self.state_change_check()

    def withdraw(self, amount):
        self.balance -= amount
        self.state_change_check()

    def pay_interest(self):
        self.balance += self._interest * self.balance
        self.state_change_check()

    def state_change_check(self):
        if self.balance < 0.0:
            self.account.state = RedState(self)
        elif self.balance < self._lower_limit:
            self.account.state = SilverState(self)


#  Gold indicates an interest bearing state
class GoldState(object):
    def __init__(self, state):
        self.balance = state.balance
        self.account = state.account
        self._initialize()

    def _initialize(self):
        self._interest = 0.05
        self._lower_limit = 1000.0
        self._upper_limit = 10000000.0

    def deposit(self, amount):
        self.balance += amount
        self.state_change_check()

    def withdraw(self, amount):
        self.balance -= amount
        self.state_change_check()

    def pay_interest(self):
        self.balance += self._interest * self.balance
        self.state_change_check()

    def state_change_check(self):
        if self.balance < self._lower_limit:
            self.account.state = RedState(self)
        elif self.balance > self._upper_limit:
            self.account.state = GoldState(self)


# Context: defines the interface of interest to clients.
# maintains an instance of a ConcreteState subclass that defines the current state.
class Account:
    _state = None
    _owner = None

    def __init__(self, owner):
         self._owner = owner
         self._state = SilverState(0.0, self)

    @property
    def balance(self):
        return self._state.balance

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        self._state = value

    def deposit(self, amount):
        self._state.deposit(amount)
        print("Deposited {} ---".format(amount))
        print(" Balance = {}".format(self.balance))
        print(" Status = {}".format(type(self.state).__name__))
        print("")

    def withdraw(self, amount):
        self._state.withdraw(amount)
        print("Withdrew {} ---".format(amount))
        print(" Balance = {}".format(self.balance))
        print(" Status = {}".format(type(self.state).__name__))

    def pay_interest(self):
        self._state.pay_interest()
        print("Interest Paid --- ")
        print(" Balance = {}".format(self.balance))
        print(" Status = {}".format(type(self.state).__name__))


# usage
account = Account("Jim Johnson")

account.deposit(500.0)
account.deposit(300.0)
account.deposit(550.0)
account.pay_interest()
account.withdraw(2000.0)
account.withdraw(1100.00)