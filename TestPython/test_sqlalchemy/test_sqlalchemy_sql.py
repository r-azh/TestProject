#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'R.Azh'

# SQLAlchemy consists of several components:
#  Engine:The engine is an abstraction of the database and its API. It works with the connection pool and the Dialect
# component to deliver the SQL statements from the SQLAlchemy to the database. The engine is created using the
# create_engine() function. It can be used to directly interact with a database, or can be passed to a Session object
# to work with the object-relational mapper.

# Dialect: is the system SQLAlchemy uses to communicate with various types of DBAPI implementations and databases.
# All dialects require that an appropriate DBAPI driver is installed. The Dialect is created from the supplied
# connection string.

# MetaData comprises of Python objects that describe tables and other schema-level objects. Database metadata can be
# expressed by explicitly naming the various components and their properties, using constructs such as Table, Column,
# or ForeignKey. MetaData can be easily generated by SQLAlchemy using a process called reflection.

# Session: inside the ORM, the primary interface for persistence operations is the Session. The Session establishes all
# conversations with the database and represents a container for all the objects which we have loaded or associated
# with it during its lifespan. It provides the entry point to acquire a Query object, which sends queries to the
# database using the Session object’s current database connection, populating result rows into objects that are then
# stored in the Session.

# objects are always “owned” by a session and keyed by primary key. Each primary key can only exist once. Because that
#  session is quite fundamental and needs to work in many setups this is configurable
print('############################## get version ##############################')

import sqlalchemy

print(sqlalchemy.__version__)

print('############################## connect to db ##############################')

from sqlalchemy import create_engine
eng = create_engine('postgresql+psycopg2://postgres:123456@localhost/postgres')
con = eng.connect()

rs = con.execute("SELECT VERSION()")
print(rs.fetchone())

# con.close()

print('############################ using sql queries ############################')

print('           $$$$$$$$$$$$$$$ create db $$$$$$$$$$$$$$$$$')
# postgres does not allow you to create databases inside transactions, and sqlalchemy always tries to run queries in a
#  transaction. To get around this, get the underlying connection from the engine:
# conn = engine.connect()
# But the connection will still be inside a transaction, so you have to end the open transaction with a commit:

# con.execute("commit")

# And you can then proceed to create the database using the proper PostgreSQL command for it.
# con.execute("create database yaml.yml")
# con.close()

try:
    eng2 = create_engine('postgresql+psycopg2://postgres:123456@localhost/test7')
    con = eng.connect()
except Exception as ex:
    eng = create_engine('postgresql+psycopg2://postgres:123456@localhost/postgres')
    con = eng.connect()
    con.execute("commit")
    con.execute("create database test7")
    con.close()
    eng = create_engine('postgresql+psycopg2://postgres:123456@localhost/test7')
    con = eng.connect()


print('           $$$$$$$$$$$$$$$ create table $$$$$$$$$$$$$$$$$')

with eng.connect() as con:
    con.execute('DROP TABLE IF EXISTS Cars')
    con.execute('CREATE TABLE Cars(Id INTEGER PRIMARY KEY, "Name" VARCHAR(20), Price INTEGER)')

print('           $$$$$$$$$$$$$$$ insert into table $$$$$$$$$$$$$$$$$')

data = ({'Id': 1, 'Name': 'Audi', 'Price': 52642},
        {"Id": 2, "Name": "Mercedes", "Price": 57127},
        {"Id": 3, "Name": "Skoda", "Price": 9000},
        {"Id": 4, "Name": "Volvo", "Price": 29000},
        {"Id": 5, "Name": "Bentley", "Price": 350000},
        {"Id": 6, "Name": "Citroen", "Price": 21000},
        {"Id": 7, "Name": "Hummer", "Price": 41400},
        {"Id": 8, "Name": "Volkswagen", "Price": 21600}
        )
with eng.connect() as con:
    for line in data:
        # con.execute('INSERT INTO Cars(Id, "Name", Price) VALUES({Id}, {Name}, {Price})'.format(**line)) # don't work
        con.execute('INSERT INTO Cars(Id, "Name", Price) VALUES(%(Id)s, %(Name)s, %(Price)s)', **line)

    print('           $$$$$$$$$$$$$$$ select from table $$$$$$$$$$$$$$$$$')

    rs = con.execute('SELECT * FROM Cars')
    print('list of column names: ', rs.keys())
    for row in rs:
        print(row)

    print('           $$$$$$$$$$$$$$$ update in table $$$$$$$$$$$$$$$$$')
    price, id = 1235000, 1
    rs = con.execute('UPDATE Cars SET Price=%s WHERE Id=%s', (price, id))
    print(rs)

    rs = con.execute('SELECT * FROM Cars WHERE Id=%s', (id,))
    print([row for row in rs])

    print('           $$$$$$$$$$$$$$$ delete from table $$$$$$$$$$$$$$$$$')
    con.execute('DELETE FROM Cars WHERE Id=%(id)s', {'id': id})
    rs = con.execute('SELECT * FROM Cars')
    print([row for row in rs])

    print('           $$$$$$$$$$$$$$$ drop table $$$$$$$$$$$$$$$$$')
    con.execute('''DROP TABLE Cars''')


