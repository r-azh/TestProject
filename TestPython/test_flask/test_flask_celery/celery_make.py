# Celery is a task queue for Python with batteries included. It used to have a Flask integration but it became
# unnecessary after some restructuring of the internals of Celery with Version 3.
#
# A Celery installation has three core components:
#
#  -The Celery client. This is used to issue background jobs. When working with Flask, the client runs with the Flask
# application.
#  -The Celery workers. These are the processes that run the background jobs. Celery supports local and remote workers,
# so you can start with a single worker running on the same machine as the Flask server, and later add more workers as
# the needs of your application grow.
#  -The message broker. The client communicates with the the workers through a message queue, and Celery supports
# several ways to implement these queues. The most commonly used brokers are RabbitMQ and Redis.


# The first thing you need is a Celery instance, this is called the celery application. It serves the same purpose as
#  the Flask object in Flask, just for Celery. Since this instance is used as the entry-point for everything you want
#  to do in Celery, like creating tasks and managing workers, it must be possible for other modules to import it.

# For instance you can place this in a tasks module. While you can use Celery without any reconfiguration with Flask,
#  it becomes a bit nicer by subclassing tasks and adding support for Flask’s application contexts and hooking it up
#  with the Flask configuration.

from celery import Celery


def make_celery(app):
    celery = Celery(app.import_name, backend=app.config['CELERY_RESULT_BACKEND'], broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery


# The function creates a new Celery object, configures it with the broker from the application config, updates the
#  rest of the Celery config from the Flask config and then creates a subclass of the task that wraps the task
#  execution in an application context.
