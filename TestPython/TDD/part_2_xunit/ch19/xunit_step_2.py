

class TestCase:
    def __init__(self, name):
        self.name = name

    def run(self):
        self.setUp()
        method = getattr(self, self.name)
        method()

    def setUp(self):
        pass


class WasRun(TestCase):
    def __init__(self, name):
        self.was_setup = None
        self.was_run = None
        TestCase.__init__(self, name)

    def test_method(self):
        self.was_run = 1

    def setUp(self):
        self.was_run = None
        self.was_setup = 1
        # Calling setUp is the job of the TestCase


class TestCaseTest(TestCase):
    def setUp(self):
        self.test = WasRun("test_method")
        # Used  setUp() to simplify the test cases checking the example test case (I told you this would become like
        # self-brain-surgery.)

    def test_running(self):
        self.test.run()
        assert self.test.was_run

    def test_setup(self):
        self.test.run()
        assert self.test.was_setup


TestCaseTest("test_running").run()
TestCaseTest("test_setup").run()
# Each test method is run in a clean instance of  TestCaseTest , so there is no way the two tests can be coupled.

# ToDo list:
# --- Invoke test method ---
# >> Invoke setUp first
# Invoke tearDown afterward
# Invoke tearDown even if the test method fails
# Run multiple tests
# Report collected results
