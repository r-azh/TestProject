# pip install pytest


#  define conftest.py with celery configs for test
from TestPython.test_celery.tests.tasks import add, mul


def test_add_task(celery_session_worker):
    assert add.delay(2, 2).get() == 4


def test_mul_task(celery_session_worker):
    assert mul.delay(3, 3).get() == 9


def test_multiple_tasks(celery_session_worker):
    add.delay(2, 5)
    mul.delay(3, 5)
    assert add.apply_async(args=[1, 1]).get() == mul.apply_async(args=[1, 2]).get()

#  to run
# cd TestPython/test_celery/tests/pytest/
# pytest test_celery_redis_pytest.py
# or add a pytest with this path in edit-configuration pycharm

