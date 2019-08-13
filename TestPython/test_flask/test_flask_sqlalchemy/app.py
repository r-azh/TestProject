__author__ = 'R.Azh'
from flask_sqlalchemy import SQLAlchemy

from flask import Flask
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:123456@127.0.0.1/postgres'

db = SQLAlchemy(app)
