__author__ = 'R.Azh'

from flask import Flask

app = Flask(__name__)
from TestPython.test_flask.test_flask_helloWorld.app import views
