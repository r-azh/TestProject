__author__ = 'R.Azh'

# A way to include language elements in a program
# Given a language, define a representation for its grammar along with an interpreter that uses the representation
# to interpret sentences in the language.

# this program converts a Roman numeral to a decimal


# AbstractExpression: declares an interface for executing an operation
class Expression:

    def one(self):
        raise NotImplementedError

    def four(self):
        raise NotImplementedError

    def five(self):
        raise NotImplementedError

    def nine(self):
        raise NotImplementedError

    def multiplier(self):
        raise NotImplementedError

    def interpret(self, context):
        if len(context.input) == 0:
            return
        if context.input.startswith(self.nine()):
            context.output += 9 * self.multiplier()
            context.input = context.input[2:]

        if context.input.startswith(self.four()):
            context.output += 4 * self.multiplier()
            context.input = context.input[2:]

        if context.input.startswith(self.five()):
            context.output += 5 * self.multiplier()
            context.input = context.input[1:]

        if context.input.startswith(self.one()):
            context.output += self.multiplier()
            context.input = context.input[1:]


# TerminalExpression: implements an Interpret operation associated with terminal symbols in the grammar.
# an instance is required for every terminal symbol in the sentence.
class ThousandExpression(Expression):
    def one(self):
        return "M"

    def four(self):
        return " "

    def five(self):
        return " "

    def nine(self):
        return " "

    def multiplier(self):
        return 1000


class HundredExpression(Expression):
    def one(self):
        return "C"

    def four(self):
        return "CD"

    def five(self):
        return "D"

    def nine(self):
        return "CM"

    def multiplier(self):
        return 100


class TenExpression(Expression):
    def one(self):
        return "X"

    def four(self):
        return "XL"

    def five(self):
        return "L"

    def nine(self):
        return "XC"

    def multiplier(self):
        return 10


class OneExpression(Expression):
    def one(self):
        return "I"

    def four(self):
        return "IV"

    def five(self):
        return "V"

    def nine(self):
        return "Ix"

    def multiplier(self):
        return 1


# NonterminalExpression: one such class is required for every rule R ::= R1R2...Rn in the grammar
# maintains instance variables of type AbstractExpression for each of the symbols R1 through Rn.
# implements an Interpret operation for nonterminal symbols in the grammar. Interpret typically calls itself
# recursively on the variables representing R1 through Rn.


# Context: contains information that is global to the interpreter
class Context:
    _input = None
    _output = None

    def __init__(self, input):
        self._input = input
        self._output = 0

    @property
    def input(self):
        return self._input

    @input.setter
    def input(self, value):
        self._input = value

    @property
    def output(self):
        return self._output

    @output.setter
    def output(self, value):
        self._output = value


# Client: builds (or is given) an abstract syntax tree representing a particular sentence in the language that the
# grammar defines. The abstract syntax tree is assembled from instances of the NonterminalExpression and
# TerminalExpression classes
# invokes the Interpret operation

roman = "MCMXXVIII"
context = Context(roman)

tree = [ThousandExpression(), HundredExpression(), TenExpression(), OneExpression()]


for exp in tree:
    exp.interpret(context)

print("{}: {}".format(roman,context.output))