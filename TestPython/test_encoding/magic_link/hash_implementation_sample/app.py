from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:HD2w2MZQTURv9w7EgNP6tj84@10.0.0.6/postgres'

db = SQLAlchemy(app)


# def create_production_app():
#     app = Flask(__name__)
#     app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
#     app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#     app.config['SECRET_KEY'] = SECRET_KEY
#     db.init_app(app)
#     app.app_context().push()  # this does the binding
#     return app


# def create_test_app():
#     app = Flask(__name__)
#     app.config['TESTING'] = True
#     app.config['SQLALCHEMY_DATABASE_URI'] = TEST_DATABASE_URL
#     app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#     app.config['SECRET_KEY'] = SECRET_KEY
#     db.init_app(app)
#     app.app_context().push()
#     return app