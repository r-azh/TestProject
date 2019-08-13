import unittest

from TestPython.TDD.part_1_money_example.ch03.multi_currency import Dollar

# we get rid of duplication between the test code and the working code


class TestMultiCurrency(unittest.TestCase):
    def test_multiplication(self):
        five = Dollar(5)
        product = five.times(2)
        self.assertEqual(10, product.amount)
        product = five.times(3)
        self.assertEqual(15, product.amount)

    def test_equality(self):
        # self.assertTrue(Dollar(5).equals(Dollar(5)))
        self.assertTrue(Dollar(5) == (Dollar(5)))
        # If two receiving stations at a known distance from each other can both measure the direction of a radio
        #  signal, then there is enough information to calculate the range and bearing of the signal. This calculation
        #  is called Triangulation. By analogy, when we triangulate, we only generalize code when we have two examples
        # or more. We briefly ignore the duplication between test and  model code. When the second example demands a
        # more general solution, then and only then do we generalize. p18
        # self.assertFalse(Dollar(5).equals(Dollar(6)))    # triangulation
        self.assertFalse(Dollar(5) == (Dollar(6)))    # triangulation


if __name__ == '__main__':
    unittest.main()


# checklist:
# --------------------------------
# $5 + 10 CHF = $10 if rate is 2:1
# --- $5 * 2 = $10 ---
# Make "amount" private
# --- Dollar side effects? ---
# Money rounding?
# >> equals()
# hash_code() # for using in equals()
# equal null
# equal object
