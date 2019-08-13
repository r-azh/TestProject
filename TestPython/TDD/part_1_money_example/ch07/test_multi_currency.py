import unittest

from TestPython.TDD.part_1_money_example.ch07.multi_currency import Dollar, Franc


class TestMultiCurrency(unittest.TestCase):
    def test_multiplication(self):
        five = Dollar(5)
        self.assertEqual(Dollar(10), five.times(2))
        self.assertEqual(Dollar(15), five.times(3))

    def test_equality(self):
        self.assertTrue(Dollar(5) == Dollar(5))
        self.assertFalse(Dollar(5) == Dollar(6))    # triangulation
        self.assertTrue(Franc(5) == Franc(5))
        self.assertFalse(Franc(5) == Franc(6))
        self.assertFalse(Franc(5) == Dollar(5))

    def test_franc_multiplication(self):
        five = Franc(5)
        self.assertEqual(Franc(10), five.times(2))
        self.assertEqual(Franc(15), five.times(3))


if __name__ == '__main__':
    unittest.main()

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
# --- 5 CHF * 2 = 10 CHF ---
# Dollar/Franc duplication
# --- common equals ---
# common times
# >> compare Francs with Dollars
# currency? instead of comparing class names for equality : Decided not to introduce more design until we had a better motivation
