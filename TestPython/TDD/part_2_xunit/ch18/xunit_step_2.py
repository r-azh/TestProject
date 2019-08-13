# We have to differentiate the parts of our one example by dynamically invoke the testMethod. When we get the attribute
# corresponding to the name of the test case, we are returned an object which, when invoked as a function, invokes the
# method.

# Now our little  WasRun class is doing two distinct jobs: one is keeping track of whether a method was invoked or not,
# and the other is dynamically invoking the method.


class WasRun:
    def __init__(self, name):
        self.was_run = None
        self.name = name

    def test_method(self):
        self.was_run = 1

    def run(self):
        method = getattr(self, self.name)
        method()
        # Here is another general pattern of refactoring: take code that works in one instance and generalize it to work
        # in many by replacing constants with variables.


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
