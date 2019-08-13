import unittest

from TestPython.TDD.part_1_money_example.ch05.multi_currency import Dollar, Franc


class TestMultiCurrency(unittest.TestCase):
    def test_multiplication(self):
        five = Dollar(5)
        self.assertEqual(Dollar(10), five.times(2))
        self.assertEqual(Dollar(15), five.times(3))

    def test_equality(self):
        self.assertTrue(Dollar(5) == (Dollar(5)))
        self.assertFalse(Dollar(5) == (Dollar(6)))    # triangulation

    def test_franc_multiplication(self):
        five = Franc(5)
        self.assertEqual(Franc(10), five.times(2))
        self.assertEqual(Franc(15), five.times(3))


if __name__ == '__main__':
    unittest.main()

# The first test in the following list is not a one little step so we write a prerequisite for it: the last one.
# - Couldn't tackle a big test, so we invented a small test that represented progress
# - Wrote the test by shamelessly duplicating and editing
# - Even worse, made the test work by copying and editing model code wholesale
# - Promised ourselves we wouldn't go home until the duplication was gone

# checklist:
# --------------------------------
# $5 + 10 CHF = $10 if rate is 2:1
# --- $5 * 2 = $10 ---
# --- Make "amount" private ---
# --- Dollar side effects? ---
# Money rounding?
# --- equals() ---
# hash_code() # for using in equals()
# equal null
# equal object
# >> 5 CHF * 2 = 10 CHF
# Dollar/Franc duplication
# common equals
# common times
