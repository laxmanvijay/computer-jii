import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

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

class Model(Base):
    __tablename__='model'
    id = Column(Integer,primary_key=True)
    email = Column(String(250),nullable=False)
    model_type = Column(String(250),nullable=False)
    model_name = Column(String(250),nullable=False)

    def __init__(self,email,model_name,model_type):
        self.email = email
        self.model_type = model_type
        self.model_name = model_name


engine = create_engine('sqlite:///computer_jii.db')

Base.metadata.create_all(engine)