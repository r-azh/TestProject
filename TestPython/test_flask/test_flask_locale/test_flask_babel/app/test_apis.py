import requests
from flask_testing import LiveServerTestCase, TestCase

from TestPython.test_flask.test_flask_locale.test_flask_babel.app import app


class TestApis(LiveServerTestCase):
    def create_app(self):
        app.app_context().push()
        return app

    def test_server_is_up_and_running(self):
        response = requests.get(self.get_server_url())
        self.assertEqual(response.status_code, 200)

    def test_hello(self):
        url = "{}/hello".format(self.get_server_url())
        print(url)
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)


class TestApis2(TestCase):
    def create_app(self):
        app.app_context().push()
        return app

    def test_hello(self):
        response = self.client.get("/hello")
        print(response.data)
        result = response.json
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result['locale_language'], None)
        self.assertEqual(result['timezone'], None)

    def test_get_locale(self):
        headers = {"Accept-Language": 'fa'}
        response = self.client.get("/hello", headers=headers)
        print(response.data)
        result = response.json
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result['locale_language'], 'fa')
        self.assertEqual(result['timezone'], None)

    def test_retrieve_text(self):
        headers = {"Accept-Language": 'fa'}
        response = self.client.get("/texts", headers=headers)
        print(response.data.decode("utf-8"))
        self.assertEqual(response.status_code, 200)
