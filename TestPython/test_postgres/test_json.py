import psycopg2
# http://www.postgresqltutorial.com/postgresql-json/
# https://stackoverflow.com/questions/15367696/storing-json-in-database-vs-having-a-new-column-for-each-key
# http://erthalion.info/2017/12/21/advanced-json-benchmarks/
# https://www.postgresql.org/docs/9.6/datatype-json.html
# https://stackoverflow.com/questions/46510723/when-to-use-json-over-key-value-tables-in-postgres-for-billions-of-rows

try:
    conn = psycopg2.connect(database='test', user='postgres', host='localhost', password='HD2w2MZQTURv9w7EgNP6tj84')
    # if db don't exist it wont connect
    print('connected')
except psycopg2.DatabaseError:
    # You can connect to the default system database postgres and then issue your query to create the new database.
    conn = psycopg2.connect(dbname='postgres', user='postgres', host='localhost', password='HD2w2MZQTURv9w7EgNP6tj84')
    # conn.set_isolation_level(psycopg2._ext.ISOLATION_LEVEL_AUTOCOMMIT)
    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    dbname = 'test'
    cur.execute('CREATE DATABASE ' + dbname)
    cur.close()

cur2 = conn.cursor()
# text = "CREATE TABLE orders (ID serial NOT NULL PRIMARY KEY, info json NOT NULL);"
# cur2.execute(text)
# conn.commit()

# text2 = '''INSERT INTO orders (info) VALUES
# ('{ "customer": "John Doe", "items": {"product": "Beer","qty": 6}}'),
# ('{ "customer": "Lily Bush", "items": {"product": "Diaper","qty": 24}}'),
# ('{ "customer": "Josh William", "items": {"product": "Toy Car","qty": 1}}'),
# ('{ "customer": "Mary Clark", "items": {"product": "Toy Train","qty": 2}}');'''
# cur2.execute(text2)
# conn.commit()
# print('data inserted')
query = 'SELECT info FROM orders'
cur2.execute(query)
result = cur2.fetchall()
print(result)

for r in result:
    print(r[0]['customer'])

#     The operator -> returns JSON object field by rsa_key.
#     The operator ->> returns JSON object field by text.

query = "SELECT info -> 'customer' AS customer From orders;"
cur2.execute(query)
result = cur2.fetchall()
print(result)

query = "SELECT info ->> 'customer' AS customer From orders;"
cur2.execute(query)
result = cur2.fetchall()
print(result)

# Because -> operator returns a JSON object, you can chain it with the operator ->> to retrieve a specific node. For
# example, the following statement returns all products sold

query = "SELECT info -> 'items' ->> 'product' as product From orders ORDER BY product;"
cur2.execute(query)
result = cur2.fetchall()
print(result)

query = "SELECT info -> 'customer' as customer From orders WHERE info -> 'items' ->> 'product' = 'Diaper';"
cur2.execute(query)
result = cur2.fetchall()
print(result)

query = "SELECT info -> 'customer' as customer, info -> 'items' ->> 'product' AS product From orders " \
        "WHERE CAST (info -> 'items' ->> 'qty' AS INTEGER) = 2;"

cur2.execute(query)
result = cur2.fetchall()
print(result)

#
# SELECT * FROM public.memberships
# where json_data->'updates'->'outlets'-> 'telegram'->>'status' = 'inactive';
#
#
#
# SELECT * FROM public.memberships
# where exists(
# 	select from jsonb_each(json_data->'updates'->'outlets') as outlets
# 	where outlets.value->>'status' = 'inactive'
# )
# and user_id = 1
#
# select jsonb_each(json_data->'updates'->'outlets') as outlets  from public.memberships
#
#
#
#
# update public.memberships
# set json_data = jsonb_set(json_data, '{updates, outlets, sms, frequency}', '{"this"}'::jsonb, true)
# where user_id = 1

# select m.* from memberships as m, jsonb_object_keys(m.json_data->'updates'->'outlets') as k
# join outlets as o
# on o.name = k
# group by m.id, k, o.id
#
#
# select id, (json_data->'trends'->'outlets')::jsonb - 'sms' || jsonb_build_object('text', json_data->'trends'->'outlets'->'sms') from memberships
#
# CREATE OR REPLACE FUNCTION jsonb_merge2(jsonb1 JSONB, jsonb2 JSONB)
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
#
# select jsonb_merge2('{"trends": {"outlets": {"sms": {"status": "active"}, "email": {"status": "active"}, "telegram": {"status": "active"}}}, "updates": {"outlets": {"sms": {"status": "active", "frequency": 5}, "email": {"status": "active", "frequency": 10}, "telegram": {"status": "inactive", "frequency": 10}}}, "generics": {"outlets": {"sms": {"status": "active"}, "email": {"status": "active"}, "telegram": {"status": "active"}}}}'::jsonb,
# '{"trends": {"outlets": {"sms": {"status": "active"}, "email": {"status": "active"}, "telegram": {"status": "active"}}}, "updates": {"outlets": {"sms": {"status": "active", "frequency": 5}, "email": {"status": "active", "frequency": 10}, "telegram": {"status": "inactive", "frequency": 150}}}, "generics": {"outlets": {"telegram": {"status": "inactive"}}}}'::jsonb);
#
# SELECT jsonb_object_agg(d ORDER BY id)
# FROM ( VALUES
#  ( 1, '{"trends": {"outlets": {"sms": {"status": "active"}, "email": {"status": "active"}, "telegram": {"status": "active"}}}, "updates": {"outlets": {"sms": {"status": "active", "frequency": 5}, "email": {"status": "active", "frequency": 10}, "telegram": {"status": "inactive", "frequency": 10}}}, "generics": {"outlets": {"sms": {"status": "active"}, "email": {"status": "active"}, "telegram": {"status": "active"}}}}'::jsonb   ),
#  ( 2, '{"trends": {"outlets": {"sms": {"status": "active"}, "email": {"status": "active"}, "telegram": {"status": "active"}}}, "updates": {"outlets": {"sms": {"status": "active", "frequency": 5}, "email": {"status": "active", "frequency": 10}, "telegram": {"status": "inactive", "frequency": 150}}}, "generics": {"outlets": {"telegram": {"status": "active"}}}}'::jsonb )
# ) AS t(id,d);

# select * from memberships as m, jsonb_object_keys(m.json_data->'updates'->'outlets') as k
# join outlets as o
# on o.name = k
# group by m.id, k, o.id
#
#
# select id, (json_data->'trends'->'outlets')::jsonb - 'sms' || jsonb_build_object('text', json_data->'trends'->'outlets'->'sms') from memberships
#
#
# select json_data->'updates'->'outlets'->'sms' from memberships;
#
# select json_data->'updates'->'outlets' from memberships;
#
# update memberships set json_data=jsonb_set(json_data, '{updates,outlets,sms,status}', '"inactive"', true) where inbox_id=1;
#
# update memberships set json_data=jsonb_insert(json_data, '{updates,outlets}', '{"slack":{"status": "inactive"}}', false) where user_id=2;
#
# select jsonb_each(json_data->'updates'->'outlets'->'sms') as outlet from memberships;
#
# update memberships
# set json_data = jsonb_set(json_data, '{updates,outlets,sms,status}', '"inactive"' )
# where json_data->'updates'->'outlets'->'sms'-> 'status'='"active"';
# ------------
# create table example(id num primary rsa_key, js jsonb);
# insert into example values
#     (1, '{"nme": "test"}'),
#     (2, '{"nme": "second test"}');
#
# update example
# set js = js - 'nme' || jsonb_build_object('name', js->'nme')
# where js ? 'nme'
# returning *;
