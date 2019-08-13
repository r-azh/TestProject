from unittest import TestCase


class TestFibonacci(TestCase):
    def test_fibonacci(self):
        cases = [
            (0, 0),
            (1, 1),
            (2, 1),
            (3, 2)
        ]
        for case in cases:
            self.assertEqual(case[1], fib(case[0]))


def fib(n: int):
    if n == 0:
        return 0
    if n <= 2:
        return 1
    return fib(n - 1) + fib(n - 2)
