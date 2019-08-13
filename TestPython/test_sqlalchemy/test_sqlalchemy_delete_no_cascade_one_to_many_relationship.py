from sqlalchemy import Column, Integer, String, ForeignKey, create_engine, Table, ForeignKeyConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

Base = declarative_base()

relation_user_address = Table(
    'relation_user_address',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), nullable=False),
    Column('address_id', Integer, ForeignKey('addresses.id'), nullable=False),
    ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    ForeignKeyConstraint(['address_id'], ['addresses.id'], ondelete='CASCADE')
)


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    password = Column(String)
    addresses = relationship('Address', secondary=relation_user_address, backref='users'
                             , single_parent=True)

    def __repr__(self):
        return "<User(name='%s', fullname='%s', password'%s')>" % \
               (self.name, self.fullname, self.password)


class Address(Base):
    __tablename__ = 'addresses'
    id = Column(Integer, primary_key=True)
    email_address = Column(String, nullable=False)

    def __repr__(self):
        return "<Address(email_address='%s')>" % self.email_address


engine = create_engine('postgresql+psycopg2://postgres:123123@localhost/postgres')
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
session = Session()

# create_above_tables
Base.metadata.create_all(bind=engine)

session.query(Address).delete()     # delete all users
session.query(User).delete()     # delete all users

session.add_all([
    User(name='wendy', fullname='Wendy Williams', password='foobar'),
    User(name='mary', fullname='Mary Contrary', password='xxg527'),
    User(name='fred', fullname='Fred Flinstone', password='blah')])

jack = User(name='jack', fullname='Jack Bean', password='gjffdd')
jack.addresses = [Address(email_address='jack@google.com'),
                  Address(email_address='j25@yahoo.com')]
session.add(jack)
session.commit()

session.delete(jack)
# session.query(Address).filter(Address.user_id==jack.id).delete()
session.commit()

count1 = session.query(User).filter_by(name='jack').count()
print(count1)

count2 = session.query(Address).count()
print(count2)
