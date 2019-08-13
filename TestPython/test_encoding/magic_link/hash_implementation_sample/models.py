from datetime import datetime

from sqlalchemy import ForeignKey, UniqueConstraint, PrimaryKeyConstraint
from sqlalchemy.ext.associationproxy import association_proxy

from interactive_secure_links.python.hash.hash_implementation_sample.app import db
from sqlalchemy.dialects.postgresql import JSONB


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True, index=True)
    password = db.Column(db.String(54))

    def __init__(self, firstname, lastname, email, password):
        self.firstname = firstname.title()
        self.lastname = lastname.title()
        self.email = email.lower()
        self.password = password


class InteractiveSecureLinkHash(db.Model):
    __tablename__ = 'interactive_secure_link_hashes'

    hash = db.Column(db.String(100), primary_key=True, autoincrement=False)
    create_ts = db.Column(db.DateTime, default=datetime.utcnow)
    expiry_ts = db.Column(db.DateTime, index=True)
    usage_limit = db.Column(db.Integer)
    user_id = db.Column(db.Integer, ForeignKey(
        'users.id',
        name='interactive_secure_link_hash_user_foreign_key',
        ondelete='CASCADE'
    ), index=True)
    module_id = db.Column(db.String(200))
    parameters_json = db.Column(JSONB, default={})

    def __init__(self, hash, expiry_ts, user_id, module_id, parameters_json, usage_limit):
        self.hash = hash
        self.expiry_ts = expiry_ts
        self.user_id = user_id
        self.module_id = module_id
        self.parameters_json = parameters_json
        self.usage_limit = usage_limit if usage_limit is not None else 0


class InteractiveSecureLinkHashAccessLog(db.Model):
    __tablename__ = 'interactive_secure_link_hashes_access_log'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    hash = db.Column(db.String(100), ForeignKey(
        'interactive_secure_link_hashes',
        name='interactive_secure_link_hash_access_log_hash_foreign_key',
        ondelete='CASCADE'
    ), index=True)
    access_ts = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, hash):
        self.hash = hash]


class InteractiveSecureLinkHashTotalAccess(db.Model):
    __tablename__ = 'interactive_secure_link_hashes_total_access'

    hash = db.Column(db.String(100), db.ForeignKey(
        'interactive_secure_link_hashes',
        name='interactive_secure_link_hash_access_log_hash_foreign_key',
        ondelete='CASCADE'
    ), primary_key=True)

    usage_count = db.Column(db.Integer)

    def __init__(self, hash, usage_count):
        self.hash = hash
        self.usage_count = usage_count
