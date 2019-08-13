
from TestPython.test_flask.test_flask_locale.test_flask_babel.app import app
# from TestPython.test_flask_locale.test_flask_babel.app import apis

[print(v.__dict__) for v in app.blueprints.values()]
app.run(host='localhost', port=8800, debug=True)
