import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from .connector import connector

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250),nullable=False)
    password = Column(String(250),nullable=False)

    def __init__(self,name,email,password):
        self.name = name
        self.email = email
        self.password = password

engine = create_engine(connector)

Base.metadata.create_all(engine)