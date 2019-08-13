from TestPython.test_flask.test_flask_sqlalchemy.app import db
from sqlalchemy.dialects.postgresql import JSONB


class Membership(db.Model):
    __tablename__ = 'memberships'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE', name='fk_user_id'), nullable=False)
    inbox_id = db.Column(db.Integer, db.ForeignKey('inboxes.id', ondelete='CASCADE', name='fk_inbox_id'), nullable=False)
    json_data = db.Column(JSONB, default='')

    def __init__(self, user_id, inbox_id, json_data):
        self.user_id = user_id
        self.inbox_id = inbox_id
        self.json_data = json_data

