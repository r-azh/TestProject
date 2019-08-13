class TestCase:
    def __init__(self, name):
        self.name = name

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


# real implementation that is not used in test
class ResultListener:
    def __init__(self):
        self.count = 0

    def start_test(self):
        self.count += 1


class TestResult:
    def __init__(self):
        self.error_count = 0
        self.run_count = 0
        self.listeners = []

    def test_started(self):
        self.run_count += 1
        for listener in self.listeners:
            listener.start_test()

    def summary(self):
        return "%d run, %d failed" % (self.run_count, self.error_count)

    def test_failed(self):
        self.error_count += 1

    def add_listener(self, listener: ResultListener):
        self.listeners.append(listener)


class TestSuit:
    def __init__(self):
        self.tests = []

    def add(self, test):
        self.tests.append(test)

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

    def test_notification(self):
        result = TestResult()
        # Why do we need a separate object for the listener? We can just use the test case itself. The TestCase
        # itself becomes a kind of Mock Object.
        # listener = ResultListener()
        self.count = 0
        # result.add_listener(listener)
        result.add_listener(self)
        WasRun("test_method").run(result)
        # assert 1 == listener.count
        assert 1 == self.count

    # self shunt: mocking ResultListener
    def start_test(self):
        self.count += 1
    # Self Shunt may require that you use Extract Interface to get an interface to implement. You will have to decide
    # whether extracting the interface is easier, or if testing the existing class as a black box is easier. I have
    # noticed, however, that interfaces extracted for shunts tend to get their third and subsequent implementations
    # soon thereafter.


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
# Suppose we wanted to dynamically update the green bar on the testing user interface. If we could connect an object to
# the  TestResult , then it could be notified when a test ran, when it failed, when a whole suite started and finished,
# and so on. Whenever we were notified that a test ran, we would update the interface.
