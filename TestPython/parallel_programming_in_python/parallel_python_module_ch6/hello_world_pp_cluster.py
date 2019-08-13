# __author__ = 'R.Azh'
#
# import os, pp
#

# The PP module implements the execution of parallel code in two ways. The first
# way considers the SMP architecture, where there are multiple processors/cores in
# the same machine. The second alternative would be distributing the tasks through
# machines in a network, configuring, and thus forming a cluster.

# def hello_world(value):
#     return "Hello world from hostname [%s] with pid [%d] and number [%d]" % (os.uname()[1], os.getpid(), value)
#
# node_list = ('192.168.25.20',)
# job_server = pp.Server(ppservers=node_list)
#
# result_dict = {}
#
# for i in xrange(10):
#     result_dict[i] = job_server.submit(hello_world, args=(i,))
#
# for key, value in result_dict.items():
#     print "key [%d] => [%s]" % (key, value())
#
#
