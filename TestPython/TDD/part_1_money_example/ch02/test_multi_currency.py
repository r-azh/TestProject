import unittest

from TestPython.TDD.part_1_money_example.ch02.multi_currency import Dollar

# we get rid of duplication between the test code and the working code


class TestMultiCurrency(unittest.TestCase):
    def test_multiplication(self):
        five = Dollar(5)
        product = five.times(2)
        self.assertEqual(10, product.amount)
        product = five.times(3)
        self.assertEqual(15, product.amount)


if __name__ == '__main__':
    unittest.main()


# checklist:
# --------------------------------
# $5 + 10 CHF = $10 if rate is 2:1
# --- $5 * 2 = $10 ---
# Make "amount" private
# >> Dollar side effects?
# Money rounding?
