import pytest


@pytest.fixture(scope='session')
def celery_config():
    import os
    print(os.getcwd())
    return {
        'broker_url': 'redis://localhost:6379/0',
        'result_backend': 'redis://localhost:6379/0',
    }
# CELERY_ALWAYS_EAGER=True


@pytest.fixture(scope='session')
def celery_includes():
    import os
    print(os.getcwd())
    return [
        'TestPython.test_celery.tests.tasks',
    ]


@pytest.fixture(scope='session')
def celery_enable_logging():
    return True

# http://alexmic.net/flask-sqlalchemy-pytest/



# from app import app, db
# @pytest.fixture(scope='session')
# def app(request):
#     app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
#     app.config['LOGGER_ENABLED'] = False
#     ctx = app.app_context()
#     ctx.push()
#
#     def teardown():
#         ctx.pop()
#
#     request.addfinalizer(teardown)
#     return app
#
#
# @pytest.fixture(scope='session')
# def db(app, request):
#     def teardown():
#         db.drop_all()
#
#     db.app = app
#     db.create_all()
#
#     request.addfinalizer(teardown)
#     return db
#
#
# @pytest.fixture(scope='function')
# def session(db, request):
#     """Creates a new database session for a test."""
#     connection = db.engine.connect()
#     transaction = connection.begin()
#
#     options = dict(bind=connection, binds={})
#     session = db.create_scoped_session(options=options)
#
#     db.session = session
#
#     def teardown():
#         transaction.rollback()
#         connection.close()
#         session.remove()
#
#     request.addfinalizer(teardown)
#     return session