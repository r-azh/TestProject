
from unittest import TestCase, mock

from TestPython.test_unit_test.helper_worker import Worker, Helper


class TestWorkerModule(TestCase):

    def test_patching_class(self):
        with mock.patch('worker.Helper') as MockHelper:
            MockHelper.return_value.get_path.return_value = 'testing'
            worker = Worker()
            MockHelper.assert_called_once_with('db')
            self.assertEqual(worker.work(), 'testing')

            #     Worker calls Helper with "db"
    # Worker returns the expected path supplied by Helper