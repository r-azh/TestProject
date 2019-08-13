import traceback
from http import HTTPStatus
from unittest import TestCase

from TestPython.test_flask.test_flask_json_schema.app import app


class TestApp(TestCase):

    def setUp(self):
        app.app_context().push()
        self.client = app.test_client()
        return app

    def test_should_return_no_error_for_user_with_correct_schema(self):
        result = self.client.get('/users/1')
        self.print_test_result(result)
        assert result.status_code == HTTPStatus.OK

    def test_should_not_create_user_with_incorrect_schema(self):
        result = self.client.get('/users/2')
        self.print_test_result(result)
        assert result.status_code == HTTPStatus.INTERNAL_SERVER_ERROR

    def test_should_not_create_user_with_incorrect_schema_absent_key(self):
        result = self.client.get('/users/3')
        self.print_test_result(result)
        assert result.status_code == HTTPStatus.INTERNAL_SERVER_ERROR

    def test_should_not_create_user_with_incorrect_schema_incorrect_type(self):
        result = self.client.get('/users/4')
        self.print_test_result(result)
        assert result.status_code == HTTPStatus.INTERNAL_SERVER_ERROR

    def print_test_result(self, result):
        print()
        traceback_ = traceback.extract_stack()
        print(traceback_[-2].name, ":  ", result.data)
