__author__ = 'R.Azh'

# Decouple an abstraction from its implementation so that the two can vary independently.
# The implementation can evolve without changing clients which use the abstraction of the object


# Abstraction: defines the abstraction's interface. maintains a reference to an object of type Implementor.
class CustomerBase:
    _data_object = None
    _group = None

    def __init__(self, group):
        self._group = group

    @property
    def data_object(self):
        return self._data_object

    @data_object.setter
    def data_object(self, value):
        self._data_object = value

    def next(self):
        self._data_object.next_record()

    def prior(self):
        self._data_object.prior_record()

    def add(self, customer):
        self._data_object.add_record(customer)

    def delete(self, customer):
        self._data_object.delete_record(customer)

    def show(self):
        self._data_object.show_record()

    def show_all(self):
        print("Customer Group: ", self._group)
        self._data_object.show_all_records()


# RefinedAbstraction: extends the interface defined by Abstraction.
class Customers(CustomerBase):
    def __init__(self, group):
        super().__init__(group)

    def show_all(self):
        print()
        print("------------------------")
        super().show_all()
        print("------------------------")


# Implementor: defines the interface for implementation classes. This interface doesn't have to correspond exactly
# to Abstraction's interface; in fact the two interfaces can be quite different. Typically the Implementation interface
#  provides only primitive operations, and Abstraction defines higher-level operations based on these primitives.

class DataObject:
    def next_record(self):
        raise NotImplementedError

    def prior_record(self):
        raise NotImplementedError

    def add_record(self, customer):
        raise NotImplementedError

    def delete_record(self, customer):
        raise NotImplementedError

    def show_record(self):
        raise NotImplementedError

    def show_all_records(self):
        raise NotImplementedError


# ConcreteImplementor: implements the Implementor interface and defines its concrete implementation
class CustomerData(DataObject):
    _customers = None
    _current = None

    def __init__(self):
        self._current = 0
        self._customers = []
        self._customers.append("Jim Jones")
        self._customers.append("Samual Jackson")
        self._customers.append("Allen Good")
        self._customers.append("Ann Stills")
        self._customers.append("Lisa Giolani")

    def next_record(self):
        if self._current <= len(self._customers) - 1:
            self._current += 1

    def prior_record(self):
        if self._current > 0 :
            self._current -= 1

    def add_record(self, customer):
        self._customers.append(customer)

    def delete_record(self, customer):
        self._customers.remove(customer)

    def show_record(self):
        print(self._customers[self._current])

    def show_all_records(self):
        for customer in self._customers:
            print(customer)


###################### usage ##############################


customers = Customers("Chicago")
customers.data_object = CustomerData()

customers.show()
customers.next()
customers.show()
customers.next()
customers.show()
customers.add("Henry Velasquez")
customers.show_all()