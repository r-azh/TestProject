__author__ = 'R.Azh'
from TestPython.test_flask.test_flask_helloWorld.app import app

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World"


# to see loaded apis
# [print(v.__dict__) for v in app.blueprints.values()]
