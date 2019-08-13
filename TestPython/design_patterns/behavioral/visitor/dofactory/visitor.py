__author__ = 'R.Azh'

# Represent an operation to be performed on the elements of an object structure. Visitor lets you define a new
# operation without changing the classes of the elements on which it operates.
# in Visitor pattern an object traverses an object structure and performs the same operation on each node in this
# structure. Different visitor objects define different operations.


# Visitor: declares a Visit operation for each class of ConcreteElement in the object structure. The operation's name
# and signature identifies the class that sends the Visit request to the visitor. That lets the visitor determine the
# concrete class of the element being visited. Then the visitor can access the elements directly through its particular
# interface
class IVisitor:
    def visit(self, element):
        raise NotImplementedError


# ConcreteVisitor: implements each operation declared by Visitor. Each operation implements a fragment of the algorithm
#  defined for the corresponding class or object in the structure. ConcreteVisitor provides the context for the
# algorithm and stores its local state. This state often accumulates results during the traversal of the structure.
class IncomeVisitor(IVisitor):
    def visit(self, element):
        employee = element
        employee.income *= 1.10
        print("{} {}'s new income is: {}".format(type(employee).__name__, employee.name, employee.income))


class VacationVisitor(IVisitor):
    def visit(self, element):
        employee = element
        employee.vacation_days += 3
        print("{} {}'s new vacation days is: {}".format(type(employee).__name__, employee.name, employee.vacation_days))


# Element: defines an Accept operation that takes a visitor as an argument.
class Element:
    def accept(self, visitor):
        raise NotImplementedError


# ConcreteElement: implements an Accept operation that takes a visitor as an argument
class Employee(Element):
    _name = None
    _income = None
    _vacation_days = None

    def __init__(self, name, income, vacation_days):
        self._name = name
        self._income = income
        self._vacation_days = vacation_days

    @property
    def name(self):
        return self._name

    @property
    def income(self):
        return self._income

    @property
    def vacation_days(self):
        return self._vacation_days

    @name.setter
    def name(self, value):
        self._name = value

    @income.setter
    def income(self, value):
        self._income = value

    @vacation_days.setter
    def vacation_days(self, value):
        self._vacation_days = value

    def accept(self, visitor):
        visitor.visit(self)


# ObjectStructure: can enumerate its elements
# may provide a high-level interface to allow the visitor to visit its elements
# may either be a Composite (pattern) or a collection such as a list or a set
class Employees:
    _employees = None

    def __init__(self):
        self._employees = []

    def attach(self, employee):
        self._employees.append(employee)

    def detach(self, employee):
        self._employees.remove(employee)

    def accept(self, visitor):
        for employee in self._employees:
            employee.accept(visitor)


# Three employee types
class Clerk(Employee):
    pass


class Director(Employee):
    pass


class President(Employee):
    pass


# usage
employees = Employees()
employees.attach(Clerk("Hank", 25000.0, 14))
employees.attach(Director("Elly", 35000.0, 16))
employees.attach(President("Dick", 45000.0, 21))

employees.accept(IncomeVisitor())
employees.accept(VacationVisitor())

