# from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
# from sqlalchemy.sql import select
#
# from TestPython.test_flask_sqlalchemy.models import User
# from TestPython.test_flask_sqlalchemy.test_json import Membership

# metadata = MetaData()
#
#
#
# view = Table('my_view', metadata)
# definition = select([Membership, User]).where(
# User.c.id == Membership.c.user_id
#  )
# create_view = CreateView(view, definition, or_replace=True)
import json

import sqlalchemy_views
from sqlalchemy import Table, orm, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql.ddl import DropTable
from sqlalchemy import MetaData, text, Column

from TestPython.test_flask.test_flask_sqlalchemy.app import db
from TestPython.test_flask.test_flask_sqlalchemy.models import Inbox, User
from TestPython.test_flask.test_flask_sqlalchemy.test_json import Membership


class View(Table):
    is_view = True


class CreateView(sqlalchemy_views.CreateView):
    def __init__(self, view):
        super().__init__(view.__view__, view.__definition__)


@compiles(DropTable, "postgresql")
def _compile_drop_table(element, compiler, **kwargs):
    if hasattr(element.element, 'is_view') and element.element.is_view:
        return compiler.visit_drop_view(element)

    # cascade seems necessary in case SQLA tries to drop
    # the table a view depends on, before dropping the view
    return compiler.visit_drop_table(element) + ' CASCADE'


class MembershipUserView:
    user_id = None              # for accessing from outside the class
    firstname = None
    lastname = None
    email = None
    membership_id = None
    inbox_id = None

    json_data = None

    __view__ = View(
        'membership_user_view', MetaData(),
        Column('user_id', db.Integer, ForeignKey('users.id'), primary_key=True),
        Column('firstname', db.String(100)),
        Column('lastname', db.String(100)),
        Column('email', db.String(120)),
        Column('membership_id', db.Integer, ForeignKey('memberships.id'), primary_key=True),
        Column('inbox_id', db.Integer, ForeignKey('inboxes.id'), primary_key=True),
        Column('json_data', JSONB)
    )
    inbox = db.relationship('Inbox', foreign_keys=[inbox_id], single_parent=True)
    user = db.relationship('User', foreign_keys=[user_id], single_parent=True)

    __definition__ = text('''select u.id user_id, u.firstname, u.lastname, u.email, m.id membership_id, m.inbox_id, m.json_data
     from users u join memberships m on u.id=m.user_id''')

db.drop_all()

# keeping track of your defined views makes things easier
views = [MembershipUserView]

db.create_all()
db.session.commit()

# Mapping the views (enable ORM functionality):
# Do when loading up your app, before any queries and after setting up the DB.

for view in views:
    if not hasattr(view, '_sa_class_manager'):
        orm.mapper(view, view.__view__)


# Creating the views:
# Do when initializing the database, e.g. after a create_all() call.


for view in views:
    db.engine.execute(CreateView(view))

# How to query a view:
admin = User.query.filter(User.email == 'admin@example.com').first()
guest = User.query.filter(User.email == 'guest@example.com').first()
inbox = Inbox.query.filter(Inbox.name == 'inbox_1').first()
if admin is None:
    admin = User('admin', 'admini', 'admin@example.com', 'passhash')
    guest = User('guest', 'guesti', 'guest@example.com', 'passhash')
    inbox = Inbox('inbox_1')
    db.session.add(admin)
    db.session.add(guest)
    db.session.add(inbox)
    db.session.commit()
    membership = Membership(user_id=admin.id, inbox_id=inbox.id, json_data=json.dumps({"status": "inactive"}))
    db.session.add(membership)
    db.session.commit()

result1 = db.session.query(MembershipUserView).all()
print(result1)
print(result1[0].firstname)
results = db.session.query(Inbox, MembershipUserView).join(
    MembershipUserView,
    Inbox.id == MembershipUserView.inbox_id
).all()
print(results)