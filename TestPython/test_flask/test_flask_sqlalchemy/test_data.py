import json

from sqlalchemy import cast, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import load_only

from TestPython.test_flask.test_flask_sqlalchemy.test_json import Membership

__author__ = 'R.Azh'

from TestPython.test_flask.test_flask_sqlalchemy.models import User, db, Inbox

# pip3 install psycopg2-binary==2.7.4

# all model table classes like User should be imported to be created.
db.create_all()
db.session.commit()

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

json_data = {
    "updates": {
        "outlets": {
            "telegram": {
                "status": "inactive",
                "frequency": 10
            },
            "sms": {
                "status": "active",
                "frequency": 5
            },
            "email": {
                "status": "active",
                "frequency": 10
            }
        }
    },
    "generics": {
        "outlets": {
            "telegram": {
                "status": "active",
            },
            "sms": {
                "status": "active",
            },
            "email": {
                "status": "active",
            }
        }
    },
    "trends": {
        "outlets": {
            "telegram": {
                "status": "active",
            },
            "sms": {
                "status": "active",
            },
            "email": {
                "status": "active",
            }
        }
    }
}
membership = Membership(user_id=admin.id, inbox_id=inbox.id, json_data=json_data)
db.session.add(membership)
db.session.commit()


membership_1 = Membership.query.filter(Membership.json_data["updates"]["outlets"]["email"]['status'] == cast("active", JSONB)).all()
print(membership_1)

membership_2 = Membership.query.filter(Membership.json_data["updates"]["outlets"]["telegram"]['status'].astext == "inactive").all()
print(membership_2)


# sqlalchemy.dialects.postgresql.JSONB.Comparator (Python class, in PostgreSQL)
# sqlalchemy.dialects.postgresql.JSONB.Comparator.contained_by (Python method, in PostgreSQL)
# sqlalchemy.dialects.postgresql.JSONB.Comparator.contains (Python method, in PostgreSQL)
# sqlalchemy.dialects.postgresql.JSONB.Comparator.has_all (Python method, in PostgreSQL)
# sqlalchemy.dialects.postgresql.JSONB.Comparator.has_any (Python method, in PostgreSQL)
# sqlalchemy.dialects.postgresql.JSONB.Comparator.has_key (Python method, in PostgreSQL)
# sqlalchemy.dialects.postgresql.JSONB.comparator_factory (Python attribute, in PostgreSQL)

# does rsa_key exists
membership_3 = Membership.query.filter(Membership.json_data.has_key('updates')).all()
print(membership_3)

# does rsa_key exists
membership_4 = Membership.query.filter(Membership.json_data.op('?')('updates')).all()
print(membership_4)

# does rsa_key exists
membership_4 = Membership.query.filter(Membership.json_data.op('?')('updates')).all()
print(membership_4)
#
# membership_5 = Membership.query.filter(Membership.json_data["updates"]["outlets"]["sms"]['frequency'].astext.cast(Integer) == 5).scalar()
# print(membership_5)

# update
membership_x = Membership.query.first()
# membership_x.json_data = func.jsonb_set(Membership.json_data, '{trends,outlets,sms}', '{"status": "inactive"}')
# or
membership_x.json_data = func.jsonb_set(Membership.json_data, '{trends,outlets,sms}', json.dumps({"status": "inactive"})) # insert or replace sms
db.session.commit()
membership = Membership.query.options(load_only(Membership.json_data)).filter(Membership.id==membership_x.id).first()
print(membership.json_data)

# membership_x.json_data = {}
# db.session.commit()


# All the items of the path parameter of jsonb_set as well as jsonb_insert except the last item must be present in the target.
# The path given in the query does not meet the above condition. Actually, jsonb_set() does not work for objects at the
#  root level, and the only way is to use the || operator:

# membership_x.json_data = func.jsonb_insert(Membership.json_data, '{trends,outlets,sms}', json.dumps({"status": "active"}))  # don't work
# if 'trends' in membership_x.json_data:
#     if 'outlets' in membership_x.json_data['trends']:
#         if 'email' in membership_x.json_data['trends']['outlets']:
#             membership_x.json_data = func.jsonb_insert(Membership.json_data,
#                                                        json.dumps({"trends": {"outlets": {"email": {"status": "active"}}}}))
# db.session.commit()

# membership_x.json_data = func.jsonb_build_object(Membership.json_data, json.dumps({"trends": {"outlets": {"email": {"status": "active"}}}})) # replaces  from trends
# db.session.commit()

# membership_x.json_data = Membership.json_data.op('||')(json.dumps({"trends": {"outlets": {"email": {"status": "active"}}}})) # replaces  from trends
# db.session.commit()


# CREATE OR REPLACE FUNCTION jsonb_merge(jsonb1 JSONB, jsonb2 JSONB)
#   RETURNS JSONB LANGUAGE sql IMMUTABLE AS
# $func$
# SELECT
# CASE
#    WHEN jsonb_typeof($1) = 'object' AND jsonb_typeof($2) = 'object' THEN
#      (
#        SELECT jsonb_object_agg(merged.rsa_key, merged.value)
#        FROM  (
#          SELECT rsa_key
#               , CASE WHEN p1.value <> p2.value          -- implies both are NOT NULL
#                      THEN jsonb_merge2(p1.value, p2.value)
#                      ELSE COALESCE(p2.value, p1.value)  -- p2 trumps p1
#                 END AS value
#          FROM   jsonb_each($1) p1
#          FULL   JOIN jsonb_each($2) p2 USING (rsa_key)      -- USING helps to simplify
#          ) AS merged
#        WHERE  merged.value IS NOT NULL                  -- simpler, might help query planner
#        AND    merged.value NOT IN ( '[]', 'null', '{}' )
#      )
#    WHEN $2 IN ( '[]', 'null', '{}' ) THEN               -- just as simple as above
#      NULL
#    ELSE
#      $2
#  END
# $func$;
# CREATE AGGREGATE jsonb_object_agg(jsonb) (
#   SFUNC = 'jsonb_concat',
#   STYPE = jsonb,
#   INITCOND = '{}'
# );

# text = Text('''
# UPDATE memberships SET json_data = (select jsonb_merge('{"trends": {"outlets": {"sms": {"status": "active"}}}}'::jsonb,
# '{"trends": {"outlets": {"sms": {"status": "inactive"}, "email": {"status": "active"}, "telegram": {"status": "active"}}}, "updates": {"outlets": {"sms": {"status": "active", "frequency": 5}}}}'::jsonb))
# where id = %d;
# ''' %membership_x.id)

# db.get_engine(app, db.get_binds()).execute(text)
# db.session.execute(text)

merge_query = db.session.query(func.public.jsonb_merge2(
    cast('{"trends": {"outlets": {"sms": {"status": "active"}, "instagram": {"status": "active", "frequency": 100}}}}',JSONB),
    cast('{"trends": {"outlets": {"sms": {"status": "inactive"}, "email": {"status": "active"}, "telegram": {"status": "active"}}}, "updates": {"outlets": {"sms": {"status": "active", "frequency": 15}}}}',JSONB)))
query = Membership.query.filter(Membership.id == membership_x.id).update({Membership.json_data: json.loads(merge_query.all()[0][0])})
db.session.commit()


membership = Membership.query.options(load_only(Membership.json_data)).filter(Membership.id==membership_x.id).first()
print(membership.json_data)

db.session.close()
# db.drop_all()
