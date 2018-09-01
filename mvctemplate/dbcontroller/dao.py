from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .connector import connector
from .dto import User, Base

engine = create_engine(connector)

Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)

session = DBSession()

def Hello():
    return "hello"