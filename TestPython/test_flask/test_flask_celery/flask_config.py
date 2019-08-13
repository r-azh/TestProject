from celery.schedules import crontab
from flask import Flask
from TestPython.test_flask.test_flask_celery.celery_make import make_celery

flask_app = Flask(__name__)
print(__name__)

flask_app.config.update(
        CELERY_BROKER_URL='redis://localhost:6379',
        CELERY_RESULT_BACKEND='redis://localhost:6379',
        CELERYBEAT_SCHEDULE={
            'test-celery': {
                'task': 'TestPython.test_flask_celery.flask_config.add',
                'args': (10, 12),
                # Every minute
                'schedule': crontab(minute="*"),
            }
        }
)

celery = make_celery(flask_app)


@celery.task()
def add(a, b):
    return a + b
