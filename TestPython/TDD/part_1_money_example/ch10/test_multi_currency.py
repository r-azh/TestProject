import unittest

from TestPython.TDD.part_1_money_example.ch10.multi_currency import Money, Franc, Dollar


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

    def test_different_class_equality(self):
        self.assertTrue(Money(10, 'CHF') == Franc(10, "CHF"))
        self.assertTrue(Money(10, 'USD') == Dollar(10, 'USD'))


if __name__ == '__main__':
    unittest.main()

# There's no obvious way to make them identical. Sometimes you have to go backward to go forward, a little like solving
# a Rubik's Cube. What happens if we inline the factory methods? (I know, I know, we just called the factory method for
# the first time just one chapter ago. Frustrating, isn't it?)

# Does it really matter whether we have a  Franc or a  Money ? We could carefully reason about this given our knowledge
# of the system, but we have clean code and we have tests that give us confidence that the clean code works. Rather than
# apply minutes of suspect reasoning, we can just ask the computer by making the change and running the tests. In
# teaching TDD, I see this situation all the time—excellent software engineers spending 5 to 10 minutes reasoning about
# a question that the computer could answer in 15 seconds. Without the tests you have no choice, you have to reason.
# With the tests you can decide whether an experiment would answer the question faster. Sometimes you should just ask
# the computer.

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
# >> common times
# --- compare Francs with Dollars ---
# --- currency? instead of comparing class names for equality ---
# Delete testFrancMultiplication?
