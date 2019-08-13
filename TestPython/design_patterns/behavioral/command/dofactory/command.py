__author__ = 'R.Azh'

# Encapsulate a command request as an object
# Encapsulate a request as an object, thereby letting you parameterize clients with different requests, queue or
# log requests, and support undoable operations.


# Command: declares an interface for executing an operation
class Command:
    def execute(self):
        raise NotImplementedError

    def unexecute(self):
        raise NotImplementedError


# ConcreteCommand: defines a binding between a Receiver object and an action
# implements Execute by invoking the corresponding operation(s) on Receiver
class CalculatorCommand(Command):
    _operator = None
    _operand = None
    _calculator = None

    def __init__(self, calculator, operator, operand):
        self._calculator = calculator
        self._operator = operator
        self._operand = operand
        self._undo = {'+': '-', '-': '+', '*': '/', '/': '*'}

    @property
    def operator(self):
        return self._operator

    @operator.setter
    def operator(self, value):
        self._operator = value

    @property
    def operand(self):
        return self._operand

    @operand.setter
    def operand(self, value):
        self._operand = value

    def execute(self):
        self._calculator.operation(self._operator, self._operand)

    def unexecute(self):
        self._calculator.operation(self._undo[self._operator], self._operand)


# Receiver: knows how to perform the operations associated with carrying out the request.
class Calculator:
    _curr = 0

    def operation(self, operator, operand):
        if operator == '+':
            self._curr += operand

        elif operator == '-':
            self._curr -= operand

        elif operator == '*':
            self._curr *= operand

        elif operator == '/':
            self._curr /= operand
        print("current value= {} (following {}{})".format(self._curr, operator, operand))


# Invoker: asks the command to carry out the request
class User:
    _calculator = None
    _commands = None
    _current = None

    def __init__(self):
        self._calculator = Calculator()
        self._commands = []
        self._current = 0

    def redo(self, levels):
        print("\n --- Redo {} levels".format(levels))
        for i in range(levels):
            if self._current < len(self._commands):
                command = self._commands[self._current]
                self._current += 1
                command.execute()

    def undo(self, levels):
        print("\n --- Undo {} levels".format(levels))
        for i in range(levels):
            if self._current > 0:
                self._current -= 1
                command = self._commands[self._current]
                command.unexecute()

    def compute(self, operator, operand):
        command = CalculatorCommand(self._calculator, operator, operand)
        command.execute()
        self._commands.append(command)
        self._current += 1


# Client: creates a ConcreteCommand object and sets its receiver

user = User()
user.compute('+', 100)
user.compute('-', 50)
user.compute('*', 10)
user.compute('/', 2)

user.undo(4)
user.redo(3)


