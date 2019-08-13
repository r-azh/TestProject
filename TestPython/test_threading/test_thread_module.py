import _thread
import time
import sys

__author__ = 'R.Azh'

# There are two different kind of threads:
# - kernel thread
# - user thread
# Kernel Threads are part of the operating system, while User-space threads are not implemented in the kernel.


# There are two modules which support the usage of threads in Python3:
# - _thread
# - threading
# The thread module has been "deprecated" for quite a long time. Users are encouraged to use the threading module
# instead. So,in Python 3 the module "thread" is not available anymore. However, it has been renamed to "_thread" for
#  backwards compatibilities in Python3.

def test_func(txt):
    print(txt)

# To spawn another thread, you need to call following method available in thread module:
# This method call enables a fast and efficient way to create new threads in both Linux and Windows.
# The method call returns immediately and the child thread starts and calls function with the passed list of agrs.
# When function returns, the thread terminates.
# Although it is very effective for low-level threading, but the thread module is very limited compared to the newer
#  threading module.

_thread.start_new_thread(test_func, ('aaa',))
_thread.start_new_thread(test_func, ('bbb',))

print("###################################\n")


# Define a function for the thread
def print_time(thread_name, delay):
    count = 0
    while count < 5:
        time.sleep(delay)
        count += 1
        print("%s: %s" % (thread_name, time.ctime(time.time())))


# Create two threads as follows
try:
    _thread.start_new_thread(print_time, ('thread_1', 1,))
    _thread.start_new_thread(print_time, ('thread_2', 2,))
except:
    print("Unexpected error:", sys.exc_info()[0])
    print("Error: unable to start thread")

# Program goes in an infinite loo. You will have to press ctrl-c to stop
while 1:
    pass

