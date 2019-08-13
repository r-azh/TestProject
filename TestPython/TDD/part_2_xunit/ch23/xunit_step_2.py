class TestCase:
    def __init__(self, name):
        self.name = name

    # Changed the interface of the run method so that the item and the Composite of items could work identically, then
    # finally got the test working
    def run(self, result):
        result.test_started()
        self.setUp()
        try:
            method = getattr(self, self.name)
            method()
        except:
            result.test_failed()
        self.tearDown()

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
    # def run(self):
    #     result = TestResult()
    #     for test in self.tests:
    #         test.run(result)
    #     return result
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
    def run(self, result):
        for test in self.tests:
            test.run(result)


class TestCaseTest(TestCase):
    def setUp(self):
        self.result = TestResult()

    def test_template_method(self):
        test = WasRun("test_method")
        test.run(self.result)
        assert 'setUp test_method tearDown ' == test.log

    def test_result(self):
        test = WasRun("test_method")
        test.run(self.result)
        assert '1 run, 0 failed' == self.result.summary()

    def test_failed_result(self):
        test = WasRun("test_broken_method")
        test.run(self.result)
        assert '1 run, 1 failed' == self.result.summary()

    def test_failed_result_formatting(self):
        self.result.test_started()
        self.result.test_failed()
        assert '1 run, 1 failed' == self.result.summary()

    def test_suit(self):
        suit = TestSuit()
        suit.add(WasRun("test_method"))
        suit.add(WasRun("test_broken_method"))
        suit.run(self.result)
        assert '2 run, 1 failed' == self.result.summary()


# ** Duplication is always a bad thing, unless you look at it as motivation to find the missing design element.**
# There is substantial duplication here, which we could eliminate if we had a way of constructing a suite automatically
# given a test class.
suit = TestSuit()
suit.add(TestCaseTest("test_template_method"))
suit.add(TestCaseTest("test_result"))
suit.add(TestCaseTest("test_failed_result_formatting"))
suit.add(TestCaseTest("test_failed_result"))
suit.add(TestCaseTest("test_suit"))
result = TestResult()
suit.run(result)
print(result.summary())

# ToDo list:
# --- Invoke test method ---
# --- Invoke setUp first ---
# --- Invoke tearDown afterward ---
# --- Invoke tearDown even if the test method fails ---
# --- Run multiple tests ---
# --- Report collected results ---
# --- Log string in WasRun ---
# --- report failed tests ---
# Catch and report setUp errors
# Create TestSuit from a TestCase class
