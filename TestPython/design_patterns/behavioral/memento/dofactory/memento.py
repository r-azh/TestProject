__author__ = 'R.Azh'

# Without violating encapsulation, capture and externalize an object's internal state so that the object can be
# restored to this state later.


# Memento: stores internal state of the Originator object. The memento may store as much or as little of the
# originator's internal state as necessary at its originator's discretion.
# protect against access by objects of other than the originator. Mementos have effectively two interfaces. Caretaker
# sees a narrow interface to the Memento -- it can only pass the memento to the other objects. Originator, in contrast,
# sees a wide interface, one that lets it access all the data necessary to restore itself to its previous state.
# Ideally, only the originator that produces the memento would be permitted to access the memento's internal state.
class Memento:
    _name = None
    _phone = None
    _budget = None

    def __init__(self, name, phone, budget):
        self._name = name
        self._phone = phone
        self._budget = budget

    @property
    def name(self):
        return self._name

    @property
    def phone(self):
        return self._phone

    @property
    def budget(self):
        return self._budget

    @name.setter
    def name(self, value):
        self._name = value

    @phone.setter
    def phone(self, value):
        self._phone = value

    @budget.setter
    def budget(self, value):
        self._budget = value


# Originator: creates a memento containing a snapshot of its current internal state.
# uses the memento to restore its internal state
class SalesProspect:
    _name = None
    _phone = None
    _budget = None

    @property
    def name(self):
        return self._name

    @property
    def phone(self):
        return self._phone

    @property
    def budget(self):
        return self._budget

    @name.setter
    def name(self, value):
        self._name = value
        print("name = ", self._name)

    @phone.setter
    def phone(self, value):
        self._phone = value
        print("phone = ", self._phone)

    @budget.setter
    def budget(self, value):
        self._budget = value
        print("budget = ", self._budget)

    def save_memento(self):
        print("\n saving state -- \n")
        return Memento(self._name, self._phone, self._budget)

    def restore_memento(self, memento):
        print("\n restoring state -- \n")
        self.name = memento.name
        self.phone = memento.phone
        self.budget = memento.budget


# Caretaker: is responsible for the memento's safekeeping
# never operates on or examines the contents of a memento.
class ProspectMemory:
    _memento = None

    @property
    def memento(self):
        return self._memento

    @memento.setter
    def memento(self, value):
        self._memento = value


# usage
s = SalesProspect()
s.name = "Noel van Halen"
s.phone = "(412) 256-0990"
s.budget = 25000.0

m = ProspectMemory()
m.memento = s.save_memento()

s.name = "Leo Welch"
s.phone = "(310) 209-7111"
s.budget = 1000000.0

s.restore_memento(m.memento)

