from sqlalchemy.engine.reflection import Inspector

__author__ = 'R.Azh'


from sqlalchemy import create_engine, inspect, Table, MetaData

engine = create_engine('postgresql+psycopg2://postgres:123456@localhost/postgres')


meta = MetaData(bind=engine)
messages = Table('users', meta, autoload=True, autoload_with=engine)
print([c.name for c in messages.columns])
print('users' in meta.tables)


# Overriding Reflected Columns
# Individual columns can be overridden with explicit values when reflecting tables; this is handy for specifying
# custom datatypes, constraints such as primary keys that may not be configured within the database


print('###################### Reflecting All Tables at Once ############################')

meta2 = MetaData()
meta2.reflect(bind=engine)
users_table = meta2.tables['users']
department_table = meta2.tables['department']


print('#################### a handy way to clear or delete all the rows in a database ###########################')
for table in reversed(meta.sorted_tables):
    engine.execute(table.delete())


print('###################### Reflection with Inspector ###########################')
# insp = Inspector.from_engine(engine)
# or
insp = inspect(engine)
print(insp.default_schema_name)
print(insp.get_schema_names())
print(insp.get_table_names())


print('###################### get current db name ############################')
print(meta._bind.engine.url.database)
print(engine.url.database)