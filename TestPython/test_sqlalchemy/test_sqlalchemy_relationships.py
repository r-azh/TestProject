import sqlalchemy

__author__ = 'R.Azh'

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy import create_engine

print('############## create db #################')
eng = create_engine('postgresql+psycopg2://postgres:123456@localhost/postgres')

# engine = create_engine("postgres://localhost/mydb")
# if not database_exists(engine.url):
#     create_database(engine.url)
con = eng.connect()
con.execute("commit")
dbname = 'test4'

if not list(con.execute("SELECT datname FROM pg_catalog.pg_database WHERE lower(datname) = lower('{}')".format(dbname))):
    print('creating db')
    con.execute("CREATE DATABASE {}".format(dbname))
# con.close()
print(con.info.keys())

eng = create_engine('postgresql+psycopg2://postgres:123456@localhost/{}'.format(dbname))
con = eng.connect()

print('############################ relationships ############################')

print('############## basic model #################')

Base = declarative_base()


class Person(Base):
    __tablename__ = 'persons'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(30))
    last_name = Column(String(30))


print('############## Many-to-One Relationships  #################')


class Manufacturer(Base):
    __tablename__ = 'manufacturers'
    id = Column(Integer, primary_key=True)
    name = Column(String(30))


class Car(Base):
    __tablename__ = 'cars'
    id = Column(Integer, primary_key=True)
    manufacturer_id = Column(Integer, ForeignKey('manufacturers.id'))
    name = Column(String(30))

    manufacturer = relationship('Manufacturer', backref=
    backref('cars', lazy='dynamic'))


print('############## Many-To-Many #################')

# When defining tables using the declarative syntax, the metadata is inherited through the class declaration from Base
# like class ChatLog(Base)
# but, when defining tables using the old Table syntax, the metadata must be explicitly specified.
pizza_toppings = Table('pizza_toppings', Base.metadata,
    Column('topping_id', Integer, ForeignKey('toppings.id')),
    Column('pizza_id', Integer, ForeignKey('pizzas.id')))


class Topping(Base):
    __tablename__ = 'toppings'
    id = Column(Integer, primary_key=True)
    name = Column(String(30))


class Pizza(Base):
    __tablename__ = 'pizzas'
    id = Column(Integer, primary_key=True)
    name = Column(String(30))

    toppings = relationship('Topping', secondary=pizza_toppings,
                            backref=backref('pizzas', lazy='dynamic'))


topping = Topping()
topping.id = 1
topping.name = 'muzzarella'

pizza = Pizza()
pizza.id = 1
pizza.name = 'pepperoni'
pizza.toppings = [topping]

# A typical lifespan of a Session looks like this:
# - A Session is constructed, at which point it is not associated with any model objects.
# - The Session receives query requests, whose results are persisted / associated with the Session.
# - Arbitrary number of model objects are constructed and then added to the Session, after which point the Session
# starts to maintain and manage those objects.
# - Once all the changes are made against the objects in the Session, we may decide to commit the changes from the
# Session to the database or rollback those changes in the Session. Session.commit() means that the changes made to the
#  objects in the Session so far will be persisted into the database while Session.rollback() means  those changes
# will be discarded.
# - Session.close() will close the Session and its corresponding connections, which means we are done with the Session
#  and want to release the connection object associated with it.

# The sessionmaker factory generates new Session objects when called
Session = sessionmaker()
# later, in a local scope, create and use a session:
# Session.configure(bind=engine)
# or
# sess = Session(bind=connection)
Base.metadata.create_all(bind=eng)
session = Session(bind=con)

session.add(topping)
session.add(pizza)



