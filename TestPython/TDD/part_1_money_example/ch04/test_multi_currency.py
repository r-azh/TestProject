import unittest

from TestPython.TDD.part_1_money_example.ch04.multi_currency import Dollar

# we get rid of duplication between the test code and the working code


class TestMultiCurrency(unittest.TestCase):
    def test_multiplication(self):
        # This test speaks to us more clearly now, as if it were an assertion of truth, not a sequence of operations
        five = Dollar(5)
        self.assertEqual(Dollar(10), five.times(2))
        self.assertEqual(Dollar(15), five.times(3))

    def test_equality(self):
        self.assertTrue(Dollar(5) == (Dollar(5)))
        self.assertFalse(Dollar(5) == (Dollar(6)))    # triangulation

        #  Notice that we have opened ourselves up to a risk. If the test for equality fails to accurately check
        # that equality is working, then the test for multiplication could also fail to accurately check that
        # multiplication is working. This is a risk that we actively manage in TDD. We aren't striving for perfection.
        # By saying everything two ways—both as code and as tests—we hope to reduce our defects enough to move forward
        # with confidence. From time to time our reasoning will fail us and a defect will slip through. When that
        # happens, we learn our lesson about the test we should have written and move on. The rest of the time we go
        # forward boldly under our bravely flapping green bar (my bar doesn't actually flap, but one can dream.)

if __name__ == '__main__':
    unittest.main()


# checklist:
# --------------------------------
# $5 + 10 CHF = $10 if rate is 2:1
# --- $5 * 2 = $10 ---
# >> Make "amount" private
# --- Dollar side effects? ---
# Money rounding?
# --- equals() ---
# hash_code() # for using in equals()
# equal null
# equal object
