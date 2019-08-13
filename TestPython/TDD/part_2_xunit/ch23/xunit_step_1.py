class TestCase:
    def __init__(self, name):
        self.name = name

    def run(self):
        result = TestResult()
        result.test_started()
        self.setUp()
        try:
            method = getattr(self, self.name)
            method()
        except:
            result.test_failed()
        self.tearDown()
        return result

    def setUp(self):
        pass

    def tearDown(self):
        pass


class WasRun(TestCase):
    def __init__(self, name):
        self.was_run = None
        TestCase.__init__(self, name)

    def test_method(self):
        self.was_run = 1
        self.log = self.log + 'test_method '

    def setUp(self):
        self.was_run = None
        self.log = 'setUp '

    def tearDown(self):
        self.log = self.log + 'tearDown '

    def test_broken_method(self):
        raise Exception


class TestResult:
    def __init__(self):
        self.error_count = 0
        self.run_count = 0

    def test_started(self):
        self.run_count += 1

    def summary(self):
        return "%d run, %d failed" % (self.run_count, self.error_count)

    def test_failed(self):
        self.error_count += 1


class TestSuit:
    def __init__(self):
        self.tests = []

    def add(self, test):
        self.tests.append(test)

    # We want a single  TestResult to be used by all of the tests that run
    def run(self):
        result = TestResult()
        for test in self.tests:
            test.run(result)
        return result
    # one of the main constraints on Composite is that the collection must respond to the same messages as the
    # individual items. If we add a parameter to  TestCase.run() , then we have to add the same parameter to
    # TestSuite.run() . I can think of three alternatives:
    # - Use Python's default parameter mechanism. Unfortunately, the default value is evaluated at compile time, not
    #   run time, and we don't want to be reusing the same  TestResult .
    # - Split the method into two parts—one that allocates the  TestResult and another which runs the test given a
    #   TestResult . I can't think of good names for the two parts of the method, which suggests that this isn't a
    #   good strategy.
    # - Allocate the  TestResult s in the caller. This pattern is called Collecting Parameter.
    # We will allocate the  TestResults in the callers.


class TestCaseTest(TestCase):
    def test_template_method(self):
        test = WasRun("test_method")
        test.run()
        assert 'setUp test_method tearDown ' == test.log

    def test_result(self):
        test = WasRun("test_method")
        result = test.run()
        assert '1 run, 0 failed' == result.summary()

    def test_failed_result(self):
        test = WasRun("test_broken_method")
        result = test.run()
        assert '1 run, 1 failed' == result.summary()

    def test_failed_result_formatting(self):
        result = TestResult()
        result.test_started()
        result.test_failed()
        assert '1 run, 1 failed' == result.summary()

    def test_suit(self):
        suit = TestSuit()
        suit.add(WasRun("test_method"))
        suit.add(WasRun("test_broken_method"))
        result = suit.run()
        assert '2 run, 1 failed' == result.summary()


# here where we invoke all of the tests, is looking pretty ratty
# ** Duplication is always a bad thing, unless you look at it as motivation to find the missing design element.**
# Here we would like the ability to compose tests and run them together. TestSuite is that it gives us a pure example of
# Composite—we want to be able to treat single tests and groups of tests exactly the same.
# We would like to be able to create a TestSuite, add a few tests to it, and then get collective results from running it
print(TestCaseTest("test_template_method").run().summary())
print(TestCaseTest("test_result").run().summary())
print(TestCaseTest("test_failed_result_formatting").run().summary())
print(TestCaseTest("test_failed_result").run().summary())
print(TestCaseTest("test_suite").run().summary())

# Wrote part of the implementation, but without making the test work. This was a violation of "da roolz." If you spotted
# it at the time, take two test cases out of petty cash. I'm sure there is a simple fake implementation that would have
# made the test case work so we could refactor under the green bar, but I can't think what it is at the moment.


# ToDo list:
# --- Invoke test method ---
# --- Invoke setUp first ---
# --- Invoke tearDown afterward ---
# --- Invoke tearDown even if the test method fails ---
# >> Run multiple tests
# --- Report collected results ---
# --- Log string in WasRun ---
# --- report failed tests ---
# catch and report setUp errors
# Create TestSuite from a TestCase class
