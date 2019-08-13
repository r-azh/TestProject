# I was going to include an implementation to ensure that  tearDown() is called regardless of exceptions during the test
# method. However, we need to catch exceptions in order to make the test work. (I know, I just tried it, and backed it
# out.) If we make a mistake implementing this, then we won't be able to see the mistake because the exceptions won't
# be reported.

# In general, the order of implementing the tests is important. When I pick the next test to implement, I find a test
# that will teach me something and which I have confidence I can make work. If I get that test working but get stuck on
# the next one, then I consider backing up two steps. It would be great if the programming environment helped me with
# this, working as a checkpoint for the code every time all of the tests run.


class TestCase:
    def __init__(self, name):
        self.name = name

    def run(self):
        result = TestResult()
        result.test_started()
        self.setUp()
        method = getattr(self, self.name)
        method()
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
        self.run_count = 0

    def test_started(self):
        self.run_count += 1

    def summary(self):
        return "%d run, 0 failed" % self.run_count


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


print(TestCaseTest("test_template_method").run().summary())
print(TestCaseTest("test_result").run().summary())
print(TestCaseTest("test_failed_result").run().summary())

# ToDo list:
# --- Invoke test method ---
# --- Invoke setUp first ---
# --- Invoke tearDown afterward ---
# Invoke tearDown even if the test method fails
# Run multiple tests
# >> Report collected results
# --- Log string in WasRun ---
