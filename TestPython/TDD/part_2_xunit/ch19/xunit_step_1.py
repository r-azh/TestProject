

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
    def test_running(self):
        test = WasRun("test_method")
        test.run()
        assert test.was_run

    def test_setup(self):
        test = WasRun("test_method")
        test.run()
        assert test.was_setup


TestCaseTest("test_running").run()
TestCaseTest("test_setup").run()
# if you want to learn something, try to figure out how we could have gotten the test to pass by changing no more than
# one method at a time.

# ToDo list:
# --- Invoke test method ---
# >> Invoke setUp first
# Invoke tearDown afterward
# Invoke tearDown even if the test method fails
# Run multiple tests
# Report collected results
