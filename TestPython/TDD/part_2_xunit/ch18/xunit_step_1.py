# First, we need to be able to create a test case and run a test method.
# We have a bootstrap # problem: we are writing test cases to test a framework that we will be using to write the test
# cases. Because we don't have a framework yet, we will have to verify the operation of the first tiny step by
# hand (printing the result and check it).

# For our first proto-test, we need a little program that will print out true if a test method gets called, and
# false otherwise. If we have a test case that sets a flag inside the test method, then we can print the flag after
# we're done and make sure it's correct. Once we have verified it manually, we can automate the process.


class WasRun:
    def __init__(self, name):
        self.was_run = None

    def test_method(self):
        self.was_run = 1

    def run(self):
        self.test_method()


test = WasRun("test_method")
print(test.was_run)
# test.test_method()
# Next we need to use our real interface,  run() , instead of calling the test method directly.
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
