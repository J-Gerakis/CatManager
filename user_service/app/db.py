import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base

engine=sqlalchemy.create_engine(f'sqlite:///jgz.db')

Base = declarative_base()