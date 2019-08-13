from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
engine = create_engine('postgresql+psycopg2://postgres:pass@localhost/postgres')
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
session = Session()