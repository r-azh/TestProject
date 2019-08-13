__author__ = 'R.Azh'

from twisted.internet import task
from twisted.internet import reactor

timeout = 60.0 # Sixty seconds

def doWork():
    #do work here
    print('tick')
    pass

l = task.LoopingCall(doWork)
l.start(timeout)     # call every sixty seconds

reactor.run()
