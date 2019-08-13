class TestCase:
    def __init__(self, name):
        self.name = name

    def run(self):
        self.setUp()
        method = getattr(self, self.name)
        method()
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


class TestCaseTest(TestCase):
    def test_template_method(self):
        test = WasRun("test_method")
        test.run()
        assert 'setUp test_method tearDown ' == test.log


TestCaseTest("test_template_method").run()

# ToDo list:
# --- Invoke test method ---
# --- Invoke setUp first ---
# >> Invoke tearDown afterward
# Invoke tearDown even if the test method fails
# Run multiple tests
# Report collected results
# >> Log string in WasRun
