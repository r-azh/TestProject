# __author__ = 'R.Azh'
#
# import os, pp


# The PP module implements the execution of parallel code in two ways. The first
# way considers the SMP architecture, where there are multiple processors/cores in
# the same machine. The second alternative would be distributing the tasks through
# machines in a network, configuring, and thus forming a cluster.

#
# def hello_world():
#     return "Hello world from [%d]" % os.getpid()
#
# job_server = pp.Server()
#
# task_result1 = job_server.submit(hello_world)
# task_result2 = job_server.submit(hello_world)
#
# print task_result1()
# print task_result2()
#
#
