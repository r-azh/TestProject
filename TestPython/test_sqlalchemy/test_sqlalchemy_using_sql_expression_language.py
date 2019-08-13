import sqlalchemy

__author__ = 'R.Azh'

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy import create_engine

eng = create_engine('postgresql+psycopg2://postgres:123456@localhost/postgres')

# engine = create_engine("postgres://localhost/mydb")
# if not database_exists(engine.url):
#     create_database(engine.url)
con = eng.connect()
con.execute("commit")
con.execute("create database test3")
con.close()


print('############################ insert using sqlalchemy objects ############################')

# SQLAlchemy schema metadata is a comprehensive system of describing and inspecting database schemas. The core of
# SQLAlchemy's query and object mapping operations is supported by database metadata.
# Metadata is information about the data in the database; for instance information about the tables and columns, in
# which we store data.

with eng.connect() as con:
    meta = sqlalchemy.MetaData(bind=eng)
    cars = sqlalchemy.Table('Cars2', meta,
                            sqlalchemy.Column('Id', sqlalchemy.Integer, primary_key=True),
                            sqlalchemy.Column('Name', sqlalchemy.String(50)),
                            sqlalchemy.Column('Price', sqlalchemy.Integer))

    print('           $$$$$$$$$$$$$$$ create table $$$$$$$$$$$$$$$$$')

    if not cars.exists(bind=con):
        cars.create(bind=con)           #  con.execute(cars.create(bind=con)) dont work

    print('           $$$$$$$$$$$$$$$ insert into table $$$$$$$$$$$$$$$$$')

    con.execute(cars.insert(), [
        {'Id': 10, 'Name': 'Audi', 'Price': 52642},
        {"Id": 20, "Name": "Mercedes", "Price": 57127},
        {"Id": 30, "Name": "Skoda", "Price": 9000},
        {"Id": 40, "Name": "Volvo", "Price": 29000},
        {"Id": 50, "Name": "Bentley", "Price": 350000},
        {"Id": 60, "Name": "Citroen", "Price": 21000},
        {"Id": 70, "Name": "Hummer", "Price": 41400},
        {"Id": 80, "Name": "Volkswagen", "Price": 21600}
    ])

    print('           $$$$$$$$$$$$$$$ select from table $$$$$$$$$$$$$$$$$')

    result = cars.select().execute()
    for row in result:
        print(row)

    print('           $$$$$$$$$$$$$$$ update in table $$$$$$$$$$$$$$$$$')

    cars.update(cars.c.Id == 20).execute(Name='**Peugeot 206**')
    result = cars.select(cars.c.Id == 20).execute()
    for row in result:
        print(row)

    print('           $$$$$$$$$$$$$$$ delete from table $$$$$$$$$$$$$$$$$')

    # column names are case sensitive
    cars.delete().where(cars.c.Id == 80).execute()
    # cars.delete().where(cars.c.Id in (10, 20, 30, 70)).execute() # dont work
    # con.query(cars).filter(cars.c.Id >= 20).delete(synchronize_session='evaluate')

    result = con.execute(cars.select())
    for row in result:
        print(row)

    con.execute(cars.delete())  # removes all rows
    result = con.execute(cars.select())
    if not row in result:
        print(result)
        print('no record!!!')

    print('           $$$$$$$$$$$$$$$ drop table $$$$$$$$$$$$$$$$$')

    cars.drop(bind=con)




