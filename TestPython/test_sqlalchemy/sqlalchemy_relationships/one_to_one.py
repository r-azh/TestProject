from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relation, relationship

from TestPython.test_sqlalchemy.sqlalchemy_relationships import Base, engine, session


class User(Base):
    __tablename__ = 'users'
    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(length=255))
    address = relationship('Address', uselist=False)


class Address(Base):
    __tablename__ = 'addresses'
    id = Column('id', Integer, primary_key=True)
    email = Column('email', String(length=255))
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', uselist=False)


for tbl in reversed(Base.metadata.sorted_tables):
    engine.execute(tbl.delete())

Base.metadata.create_all(bind=engine)


wendy = User(name='wendy')
mary = User(name='mary')
session.add(wendy)
session.add(mary)
session.commit()

address1 = Address(email="a1", user_id=wendy.id)
address2 = Address(email="a2", user_id=wendy.id)
address3 = Address(email="a3", user_id=wendy.id)
session.add(address1)
session.add(address2)
session.add(address3)
session.commit()

