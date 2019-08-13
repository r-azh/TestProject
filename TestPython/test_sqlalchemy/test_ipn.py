from sqlalchemy.ext.declarative import declarative_base

__author__ = 'R.Azh'

from sqlalchemy import create_engine
engine = create_engine('postgresql+psycopg2://postgres:123456@localhost/ipn', echo=True)

from bson import ObjectId
from sqlalchemy import Column, String

SQLAlchemyBaseModel = declarative_base()


class RegistrationMode(SQLAlchemyBaseModel):
    __tablename__ = 'registration_mode'
    _id = Column(String, primary_key=True)
    _status = Column(String)
    _label = Column(String)

    def __init__(self, object):
        self.__dict__.update(object.__dict__)
        if not self._id:
            self._id = str(ObjectId())

SQLAlchemyBaseModel.metadata.create_all(bind=engine)

RegistrationMode.__table__.drop(engine)


