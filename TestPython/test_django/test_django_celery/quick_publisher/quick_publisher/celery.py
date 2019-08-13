import os
from celery import Celery
from celery.schedules import crontab

__author__ = 'R.Azh'


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quick_publisher.settings')

app = Celery('quick_publisher')
app.config_from_object('django.conf:settings')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send_report_every_single_minute': {
        'task': 'publisher.tasks.send_view_count_report',
        'schedule': crontab(),
    }
}



# redis-server --port 6380 --slaveof 127.0.0.1 6379
# celery worker -A quick_publisher --loglevel=debug --concurrency=4

# Every time you make changes to the Celery tasks, remember to restart the Celery process. Celery needs to discover and
#  reload tasks

# Open up another console, activate the appropriate environment, and start the Celery Beat service.

# $ celery -A quick_publisher beat
# The Beat service's job is to push tasks in Celery according to the schedule.


# It's good practice to keep unreliable and time-consuming tasks outside the request time.
# Long-running tasks should be executed in the background by worker processes (or other paradigms).
# Background tasks can be used for various tasks that are not critical for the basic functioning of the application.
# Celery can also handle periodic tasks using the celery beat service.
# Tasks can be more reliable if made idempotent and retried (maybe using exponential backoff).

# Tasks are often used to perform unreliable operations, operations that depend on external resources or that can
# easily fail due to various reasons. Here's a guideline for making them more reliable:
#
# Make tasks idempotent. An idempotent task is a task that, if stopped midway, doesn't change the state of the system
# in any way. The task either makes full changes to the system or none at all.
# Retry the tasks. If the task fails, it's a good idea to try it again and again until it's executed successfully. You
# can do this in Celery with Celery Retry. One other interesting thing to look at is the Exponential Backoff algorithm.
#  This could come in handy when thinking about limiting unnecessary load on the server from retried tasks.