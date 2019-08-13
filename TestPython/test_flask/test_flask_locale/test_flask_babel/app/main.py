# pip install Flask-Babel
from flask import Flask
from flask_babel import Babel

app = Flask(__name__)
app.config.from_pyfile("settings.cfg")
babel = Babel(app)


