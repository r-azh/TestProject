import traceback
from http import HTTPStatus
from unittest import TestCase

from TestPython.test_flask.test_flask_openapi import app


class TestApp(TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_should_create_user_with_correct_schema(self):
        body = {
            "id": 1,
            "name": 'rezvan'
        }

        result = self.app.post('/users', json=body)
        self.print_test_result(result)
        assert result.status_code == HTTPStatus.CREATED

    def test_should_not_create_user_with_incorrect_schema_key(self):
        body = {
            "id_": 1,
            "name": 'rezvan'
        }

        result = self.app.post('/users', json=body)
        self.print_test_result(result)
        assert result.status_code == HTTPStatus.BAD_REQUEST

    def test_should_not_create_user_with_incorrect_schema_absent_key(self):
        body = {
            "id": 1,
        }

        result = self.app.post('/users', json=body)
        self.print_test_result(result)
        assert result.status_code == HTTPStatus.BAD_REQUEST

    def test_should_not_create_user_with_incorrect_schema_incorrect_type(self):
        body = {
            "id": 'a',
            "name": 'rezvan'
        }

        result = self.app.post('/users', json=body)
        self.print_test_result(result)
        assert result.status_code == HTTPStatus.BAD_REQUEST

    def print_test_result(self, result):
        print()
        traceback_ = traceback.extract_stack()
        print(traceback_[-2].name, ":  ", result.data)