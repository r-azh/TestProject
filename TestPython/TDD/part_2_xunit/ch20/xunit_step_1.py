# All of those flags are starting to bug me, and they are  missing an important aspect of the methods: order of calling.
# I'm going to change the testing strategy to keep a little log of the methods that are called. By always appending to
# the log, we will preserve the order in which the methods are called.


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
        self.was_run = None
        TestCase.__init__(self, name)

    def test_method(self):
        self.was_run = 1
        self.log = self.log + 'test_method '

    def setUp(self):
        self.was_run = None
        self.log = 'setUp '


class TestCaseTest(TestCase):
    def test_template_method(self):
        test = WasRun("test_method")
        test.run()
        assert 'setUp test_method ' == test.log
    #   this test is doing the work of both tests, so we can delete  test_running and rename this test and remove setUP
    # because fixtures is used in only one place

# Doing a refactoring based on a couple of early uses, then having to undo it soon after is fairly common. Some folks
# wait until they have three or four uses before refactoring because they don't like undoing work. I prefer to spend my
# thinking cycles on design, so I just reflexively do the refactorings without worrying about whether I will have to
# undo them immediately afterward.


TestCaseTest("test_template_method").run()

# ToDo list:
# --- Invoke test method ---
# --- Invoke setUp first ---
# >> Invoke tearDown afterward
# Invoke tearDown even if the test method fails
# Run multiple tests
# Report collected results
# >> Log string in WasRun
