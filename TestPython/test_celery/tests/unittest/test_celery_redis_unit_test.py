from TestPython.test_celery.tests.tasks import add, mul
import unittest


class TestAddTask(unittest.TestCase):
    def setUp(self):
        self.task = add.apply_async(args=[3, 5])
        self.results = self.task.get()

    def test_task_state(self):
        print('test_task_state')
        self.assertEqual(self.task.state, 'SUCCESS')
    #     when celery is not runnig or the task is not registered it will return 'PENDING'
    # or the test will be freezed and when debugging it will go into add function

    def test_addition(self):
        print(' test addition')
        self.assertEqual(self.results, 8)

    def test_apply(self):
        add.apply(args=[4, 5])
    # works even without running celery

    def test_multiple(self):
        mul.apply(args=[2, 3])
