import datetime

__author__ = 'R.Azh'


from celery import Celery

# todo: to run celery execute the following commands in your terminal :
# todo: 0- run redis server with command: #redis-server
# todo: 1- first cd to TestProject folder something like: cd /<path tho your projects folder>/TestProject
# todo:  ** on my pc the path is here /home//Programming/Repositories/TestProjects
# todo: 2- celery -A parsadp worker --app=TestPython.test_celery.test_celery_redis -l debug
# todo: or  go to TestPython/test_celery
# todo: then : celery -A test_celery_redis worker --loglevel=DEBUG
# todo: run this file


# The first thing you need is a Celery instance. We call this the Celery application or just app for short. As this
#  instance is used as the entry-point for everything you want to do in Celery, like creating tasks and managing
#  workers, it must be possible for other modules to import it.
broker_url = 'redis://localhost:6379/0'
result_backend = 'redis://localhost/0'
# celery_app = Celery("tasks", broker=broker_url)

# if we want to get result of the task use backend too
celery_app = Celery("tasks", broker=broker_url, backend=result_backend)

# result_backend = 'rpc://' is the The RPC result backend for AMQP brokers.
# RPC-style result backend, using reply-to and one queue per client.


# @celery_app.task()
# for tests in unit test to run we should add name="add" too
@celery_app.task(name="add")
def add(x, y):
    print("hello from test_celery_redis")
    print(x + y)
    return x + y


# To call our task you can use the delay() method. This is a handy shortcut to the apply_async() method that gives
#  greater control of the task execution
add(5, 3)
add.delay(8, 4)
add.apply_async(args=[10, 10], eta=datetime.datetime.now() + datetime.timedelta(seconds=10))

# Calling a task returns an AsyncResult instance. This can be used to check the state of the task, wait for the task to
#  finish, or get its return value (or if the task failed, to get the exception and traceback).
# Results are not enabled by default. In order to do remote procedure calls or keep track of task results in a database,
#  you will need to configure Celery to use a result backend.


# Celery, like a consumer appliance, doesn’t need much configuration to operate. It has an input and an output. The
#  input must be connected to a broker, and the output can be optionally connected to a result backend. The
# configuration can be set on the app directly or by using a dedicated configuration module. As an example you can
#  configure the default serializer used for serializing task payloads by changing the task_serializer setting

i = celery_app.control.inspect()
print(i)

s = i.scheduled()
r = i.reserved()
a = i.active()
print()