import unittest

from TestPython.TDD.part_1_money_example.ch13.multi_currency import Money, Bank, Sum


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

    def test_plus_return_sum(self):
        # Wrote a test to force the creation of an object we expected to need later ( Sum )
        five = Money.dollar(5)
        sum = five.plus(five)
        # sum = Sum(result)
        self.assertEqual(five, sum.augend)
        self.assertEqual(five, sum.addend)
        # The test above is not one I would expect to live a long time. It is deeply concerned with the implementation
        # of our operation, rather than its externally visible behavior. However, if we make it work, we expect we've
        # moved one step closer to our goal.

    def test_reduce_sum(self):
        sum = Sum(Money.dollar(3), Money.dollar(4))
        bank = Bank()
        result = bank.reduce(sum, 'USD')
        self.assertEqual(Money.dollar(7), result)

    def test_reduce_money(self):
        bank = Bank()
        result = bank.reduce(Money.dollar(1), 'USD')
        self.assertEqual(Money.dollar(1), result)


if __name__ == '__main__':
    unittest.main()

# We can't mark our test for $5 + $5 done until we've removed all of the duplication. We don't have code duplication,
# but we do have data duplication—the $10 in the fake implementation


# checklist:
# --------------------------------
# >> $5 + 10 CHF = $10 if rate is 2:1
#  >> $5 + $5 = $10     # Didn't mark a test as done because the duplication had not been eliminated
#  >> Return Money from $5 + $5
#  >> Bank.reduce(Money)
# reduce Money with conversion
# reduce(Bank, String)
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

