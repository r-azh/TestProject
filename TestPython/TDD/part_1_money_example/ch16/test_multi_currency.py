import unittest

from TestPython.TDD.part_1_money_example.ch16.multi_currency import Money, Bank, Sum


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
        self.assertEqual('USD', Money.dollar(1).currency)
        self.assertEqual('CHF', Money.franc(1).currency)

    def test_simple_addition(self):
        five = Money.dollar(5)
        sum = five.plus(five)
        bank = Bank()
        reduced = bank.reduce(sum, "USD")
        self.assertEqual(Money.dollar(10), reduced)

    def test_plus_return_sum(self):
        five = Money.dollar(5)
        sum = five.plus(five)
        self.assertEqual(five, sum.augend)
        self.assertEqual(five, sum.addend)

    def test_reduce_sum(self):
        sum = Sum(Money.dollar(3), Money.dollar(4))
        bank = Bank()
        result = bank.reduce(sum, 'USD')
        self.assertEqual(Money.dollar(7), result)

    def test_reduce_money(self):
        bank = Bank()
        result = bank.reduce(Money.dollar(1), 'USD')
        self.assertEqual(Money.dollar(1), result)

    def test_reduce_money_different_currency(self):
        bank = Bank()
        bank.add_rate('CHF', 'USD', 2)
        result = bank.reduce(Money.franc(2), 'USD')
        self.assertEqual(Money.dollar(1), result)

    def test_identity_rate(self):
        self.assertEqual(1, Bank().rate('USD', 'USD'))

    def test_mixed_addition(self):
        five_bucks = Money.dollar(5)
        ten_francs = Money.franc(10)
        bank = Bank()
        bank.add_rate('CHF', 'USD', 2)
        result = bank.reduce(five_bucks.plus(ten_francs), 'USD')
        self.assertEqual(result, Money.dollar(10))

    def test_sum_plus_money(self):
        five_bucks = Money.dollar(5)
        ten_francs = Money.franc(10)
        bank = Bank()
        bank.add_rate('CHF', 'USD', 2)
        sum = Sum(five_bucks, ten_francs).plus(five_bucks)
        result = bank.reduce(sum, 'USD')
        self.assertEqual(result, Money.dollar(15))
    #  the test is longer than the code. (You JUnit geeks will know how to fix that—the rest of you will have to
    #  read Fixture.)

    def test_sum_times(self):
        five_bucks = Money.dollar(5)
        ten_francs = Money.franc(10)
        bank = Bank()
        bank.add_rate('CHF', 'USD', 2)
        sum = Sum(five_bucks, ten_francs).times(2)
        result = bank.reduce(sum, 'USD')
        self.assertEqual(result, Money.dollar(20))

    # def test_plus_same_currency_returns_money(self):
    #     sum = Money.dollar(1).plus(Money.dollar(1))
    #     self.assertTrue(isinstance(sum, Money))
        # This test is a little ugly, because it is testing the guts of the implementation, not the externally visible
        # behavior of the objects. However, it will drive us to make the changes we need to make, and this is only an
        # experiment, after all
        # There is no obvious, clean way (not to me, anyway; I'm sure you could think of something) to check the
        # currency of the argument if and only if it is a  Money . The experiment fails, we delete the test (which we
        # didn't like much anyway), and away we go


if __name__ == '__main__':
    unittest.main()

# The three items that come up time and again as surprises when teaching TDD are:
# - The three approaches to making a test work cleanly—fake it, triangulation, and obvious implementation
# - Removing duplication between test and code as a way to drive the design
# - The ability to control the gap between tests to increase traction when the road gets slippery and cruise faster when
#   conditions are clear

# checklist:
# --------------------------------
# --- $5 + 10 CHF = $10 if rate is 2:1
# --- $5 + $5 = $10 ---
# --- Return Money from $5 + $5 ---
# --- Bank.reduce(Money) ---
# --- reduce Money with conversion ---
# reduce(Bank, String)
# >> Sum.plus
# >> Expression.times
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

