import pytest


# http://docs.celeryproject.org/en/latest/userguide/testing.html


# The celery mark enables you to override the configuration used for a single test case:
@pytest.mark.celery(result_backend='redis://')
def test_something():
    pass


@pytest.mark.celery(broker_url=config.CELERY_TEST_BROKER_URI,
                    result_backend=config.CELERY_TEST_RESULT_BACKEND_URI,
                )


@pytest.mark.celery(result_backend='redis://')
class TestSomething:

    def test_one(self):
        pass

    def test_two(self):
        ...


# celery_app - Celery app used for testing. This fixture returns a Celery app you can use for testing.
# celery_worker - Embed live worker.This fixture starts a Celery worker instance that you can use for integration tests.
#  The worker will be started in a separate thread and will be shutdown as soon as the test returns.
def test_create_task(celery_app, celery_worker):
    @celery_app.task
    def mul(x, y):
        return x*y

    assert mul.delay(4, 4).get(timeout=10) == 16
