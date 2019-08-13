from TestPython.test_flask.test_flask_celery import add

result = add.delay(23, 42)
result.wait()
