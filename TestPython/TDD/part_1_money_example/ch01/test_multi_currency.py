import unittest

from TestPython.TDD.part_1_money_example.ch01.multi_currency import Dollar

# we get rid of duplication between the test code and the working code

# The TDD cycle is as follows.
# - Add a little test.
# - Run all tests and fail.
# - Make a change.
# - Run the tests and succeed.
# - Refactor to remove duplication.


class TestMultiCurrency(unittest.TestCase):
    def test_multiplication(self):
        five = Dollar(5)
        five.times(2)
        assert five.amount == 10


if __name__ == '__main__':
    unittest.main()

# checklist
# --------------------------------
# $5 + 10 CHF = $10 if rate is 2:1
# >> $5 * 2 = $10
# Make "amount" private
# Dollar side effects?
# Money rounding?
