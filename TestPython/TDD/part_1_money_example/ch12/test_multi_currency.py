import unittest

from TestPython.TDD.part_1_money_example.ch12.multi_currency import Money, Bank


class TestMultiCurrency(unittest.TestCase):
    def test_multiplication(self):
        five = Money.dollar(5)
        self.assertEqual(Money.dollar(10), five.times(2))
        self.assertEqual(Money.dollar(15), five.times(3))

    def test_equality(self):
        self.assertTrue(Money.dollar(5) == Money.dollar(5))
        self.assertFalse(Money.dollar(5) == Money.dollar(6))    # triangulation
        self.assertFalse(Money.franc(5) == Money.dollar(5))

    def test_currency(self):
        self.assertEqual('USD', Money.dollar(1).currency())
        self.assertEqual('CHF', Money.franc(1).currency())

    def test_simple_addition(self):
        five = Money.dollar(5)
        sum = five.plus(five)
        bank = Bank()
        reduced = bank.reduce(sum, "USD")
        self.assertEqual(Money.dollar(10), reduced)


if __name__ == '__main__':
    unittest.main()

# I'm not sure how to write the story of the whole addition, so we'll start with a simpler example: $5 + $5 = $10.


# checklist:
# --------------------------------
# >> $5 + 10 CHF = $10 if rate is 2:1
#  >> $5 + $5 = $10
# --- $5 * 2 = $10 ---
# --- Make "amount" private ---
# --- Dollar side effects? ---
# Money rounding?
# --- equals() ---
# hash_code() # for using in equals()
# equal null
# equal object
# --- 5 CHF * 2 = 10 CHF ---
# --- Dollar/Franc duplication ---
# --- common equals ---
# --- common times ---
# --- compare Francs with Dollars ---
# --- currency? instead of comparing class names for equality ---
# --- Delete testFrancMultiplication? ---
