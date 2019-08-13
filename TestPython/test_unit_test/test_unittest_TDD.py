__author__ = 'R.Azh'

# TDD is about testing code you haven't yet written.define tests beÂ­fore you start coding the actual source code.
# The program developer writes an automated test case which defines the desired "behaviour" of a function.
# This test case will - that's the idea behind the approach - initially fail, because the code has still to be written.
# The major problem or difficulty of this approach is the task of writing suitable tests.

# The Python module unittest is a unit testing framework, which is based on Erich Gamma's JUnit and Kent Beck's
# Smalltalk testing framework. The module contains the core framework classes that form the basis of the test cases and
#  suites (TestCase, TestSuite and so on), and also a text-based utility class for running the tests and reporting the
# results (TextTestRunner).
# The most obvious difference to the module "doctest" consists in the fact that the test cases of the module "unittest"
#  are not defined inside of the module, which has to be tested. The major advantage is clear: program documentation
# and test descriptions are separate from each other. The price you have to pay on the other hand consists in an
#  increase of work to create the test cases


import unittest
from TestPython.test_unit_test.test_simple_unittest import fib


class FibonacciTest(unittest.TestCase):

    def setUp(self):
        self.fib_elems = ((0, 0), (1, 1), (2, 1), (3, 2), (4, 3), (5, 5))
        print("setUp executed!")

    def testCalculation(self):
        self.assertEqual(fib(0), 0)
        self.assertEqual(fib(1), 1)
        self.assertEqual(fib(5), 5)
        self.assertEqual(fib(10), 55)
        self.assertEqual(fib(20), 6765)
        for (i, val) in self.fib_elems:
            self.assertEqual(fib(i), val)

    def tearDown(self):
        self.fib_elems = None
        print("tearDown executed!")

if __name__ == "__main__":
    unittest.main()
