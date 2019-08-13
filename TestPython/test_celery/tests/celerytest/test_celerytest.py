
# celerytest provides the ability to run a Celery worker in the background from your tests. It also allows your tests
# to monitor the worker and pause until Celery tasks are completed.
from unittest import TestCase

from celerytest.testcase import CeleryTestCaseMixin, start_celery_worker
from TestPython.test_celery.tests.tasks import add, mul, celery_app

celery_app = celery_app
start_celery_worker(celery_app)    # need to setup worker outside


class TestAddTask(CeleryTestCaseMixin, TestCase):
    celery_app = celery_app
    celery_concurrency = 4

    def test_add_task(celery_session_worker):
        assert add.delay(2, 2).get() == 4

    def test_mul_task(celery_session_worker):
        assert mul.delay(3, 3).get() == 9

    def test_multiple_tasks(celery_session_worker):
        add.delay(2, 5)
        mul.delay(3, 5)
        assert add.apply_async(args=[1, 1]).get() == mul.apply_async(args=[1, 2]).get()

    def test_task_state(self):
        result = add.apply_async(args=[1, 1])
        self.assertEqual(result.state, 'SUCCESS')
        result = mul.delay(2, 3)
        self.worker.idle.wait()
        self.assertEqual(result.get(), 6)
