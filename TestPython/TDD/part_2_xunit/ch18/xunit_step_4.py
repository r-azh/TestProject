# We're getting tired of looking to see that "None" and "1" are printed every time. Using the mechanism we just built,
# we can now change test:


class TestCase:
    def __init__(self, name):
        self.name = name

    # Finally, the  run() method uses attributes from the superclass only, so it probably belongs in the superclass.
    # (I'm always looking to put the operations near the data.
    def run(self):
        method = getattr(self, self.name)
        method()


class WasRun(TestCase):
    def __init__(self, name):
        self.was_run = None
        TestCase.__init__(self, name)

    def test_method(self):
        self.was_run = 1


class TestCaseTest(TestCase):
    def test_running(self):
        test = WasRun("test_method")
        assert not test.was_run
        test.run()
        assert test.was_run


TestCaseTest("test_running").run()


# ToDo list:
# >> Invoke test method
# Invoke setUp first
# Invoke tearDown afterward
# Invoke tearDown even if the test method fails
# Run multiple tests
# Report collected results
