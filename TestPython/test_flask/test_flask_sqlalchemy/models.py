__author__ = 'R.Azh'

from TestPython.test_flask.test_flask_sqlalchemy.app import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True)
    pwdhash = db.Column(db.String(54))
    # inboxes = db.relationship('MembershipUserView', back_populates='user') # relationships wont work with views

    def __init__(self, firstname, lastname, email, password):
        self.firstname = firstname.title()
        self.lastname = lastname.title()
        self.email = email.lower()
        self.set_password(password)

    def set_password(self, password):
        self.pwdhash = (password)

    def check_password(self, password):
        return password


class Inbox(db.Model):
    __tablename__ = 'inboxes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    status = db.Column(db.String(50), default='Initialized')
    # user = db.relationship('MembershipUserView', back_populates='inbox')


    def __init__(self, name):
        self.name = name