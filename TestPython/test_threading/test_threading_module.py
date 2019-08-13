__author__ = 'R.Azh'

# The threading module exposes all the methods of the thread module and provides some additional methods:
# threading.activeCount(): Returns the number of thread objects that are active.
# threading.currentThread(): Returns the number of thread objects in the caller's thread control.
# threading.enumerate(): Returns a list of all thread objects that are currently active.
#
# In addition to the methods, the threading module has the Thread class that implements threading. The methods provided
#  by the Thread class are as follows:
# run(): The run() method is the entry point for a thread.
# start(): The start() method starts a thread by calling the run method.
# join([time]): The join() waits for threads to terminate.
# isAlive(): The isAlive() method checks whether a thread is still executing.
# getName(): The getName() method returns the name of a thread.
# setName(): The setName() method sets the name of a thread.


# To implement a new thread using the threading module, you have to do the following −
# - Define a new subclass of the Thread class.
# - Override the __init__(self [,args]) method to add additional arguments.
# - Then, override the run(self [,args]) method to implement what the thread should do when started.
# Once you have created the new Thread subclass, you can create an instance of it and then start a new thread by
#  invoking the start(), which in turn calls run() method.

import threading
import time

exit_flag = 0


class MyThread(threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        print('Starting ' + self.name)
        print_time(self.name, self.counter, 5)
        print('Exiting ' + self.name)


def print_time(thread_name, delay, counter):
    while counter:
        if exit_flag:
            thread_name.exit()
        time.sleep(delay)
        print("%s: %s" % (thread_name, time.ctime(time.time())))
        counter -= 1


# Create new threads
thread1 = MyThread(1, "Thread_1", 1)
thread2 = MyThread(2, "Thread_2", 2)

# Start Threads
thread1.start()
thread2.start()
thread1.join()
thread2.join()
print("Exiting Main Thread")
