

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

    # We'll write a smaller grained test to ensure that if we note a failed test, we print out the right results
    # If we can get the summary to print correctly when these messages are sent in this order, then our programming
    # problem is reduced to how to get these messages sent. Once they are sent, we expect the whole thing to work.
    def test_failed_result_formatting(self):
        result = TestResult()
        result.test_started()
        result.test_failed()
        assert '1 run, 1 failed' == result.summary()


print(TestCaseTest("test_template_method").run().summary())
print(TestCaseTest("test_result").run().summary())
print(TestCaseTest("test_failed_result_formatting").run().summary())
print(TestCaseTest("test_failed_result").run().summary())

# ToDo list:
# --- Invoke test method ---
# --- Invoke setUp first ---
# --- Invoke tearDown afterward ---
# Invoke tearDown even if the test method fails
# Run multiple tests
# --- Report collected results ---
# --- Log string in WasRun ---
# >> report failed tests
# catch and report setUp errors
