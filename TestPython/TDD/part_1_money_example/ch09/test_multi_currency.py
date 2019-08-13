import unittest

from TestPython.TDD.part_1_money_example.ch09.multi_currency import Money


class TestMultiCurrency(unittest.TestCase):
    def test_multiplication(self):
        five = Money.dollar(5)
        self.assertEqual(Money.dollar(10), five.times(2))
        self.assertEqual(Money.dollar(15), five.times(3))

    def test_equality(self):
        self.assertTrue(Money.dollar(5) == Money.dollar(5))
        self.assertFalse(Money.dollar(5) == Money.dollar(6))    # triangulation
        self.assertTrue(Money.franc(5) == Money.franc(5))
        self.assertFalse(Money.franc(5) == Money.franc(6))
        self.assertFalse(Money.franc(5) == Money.dollar(5))

    def test_franc_multiplication(self):
        five = Money.franc(5)
        self.assertEqual(Money.franc(10), five.times(2))
        self.assertEqual(Money.franc(15), five.times(3))

    def test_currency(self):
        self.assertEqual('USD', Money.dollar(1).currency())
        self.assertEqual('CHF', Money.franc(1).currency())


if __name__ == '__main__':
    unittest.main()

# How do we want to implement currencies at the moment? I blew it, again.
# I'll rephrase: How do we want to test for currencies at the moment?
# Were a little stuck on big design ideas, so we worked on something small we noticed earlier

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
# >> Dollar/Franc duplication
# --- common equals ---
# common times
# --- compare Francs with Dollars ---
# >> currency? instead of comparing class names for equality
# Delete testFrancMultiplication?
