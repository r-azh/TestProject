# Lots of refactoring has this feel—separating two parts so you can work on them separately. In this case, we expect to
# create a superclass TestCase.


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


test = WasRun("test_method")
print(test.was_run)
test.run()
print(test.was_run)
# We expect this to print "None" before the method was run, and "1" afterward.

# ToDo list:
# >> Invoke test method
# Invoke setUp first
# Invoke tearDown afterward
# Invoke tearDown even if the test method fails
# Run multiple tests
# Report collected results
