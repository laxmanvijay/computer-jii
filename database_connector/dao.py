from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .db_connector import connector
from .dto import User, Model, Base

engine = create_engine(connector)

Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)

session = DBSession()


def createUser(name,email,password):
    #try:
    user = User(name,email,password)
    session.add(user)
    session.commit()
    return "ok"
    #except:
    #    print("err")
    #    return "not ok"


def login(email,password):
    #try:
    user = session.query(User).filter(User.email==email).one()
    if user==None:
        return "user not exist"
    else:
        if user.password == password:
            return "password match"
        else:
            return "password do not match"
    #except:
    #    return "failed"

def getUserNameByEmail(email):
    user = session.query(User).filter(User.email==email).one()
    return user.name


def getUserModel(email):
    try:
        models = session.query(Model).filter(Model.email==email).all()
        out = []
        for model in models:
            out.append({'model_name':model.model_name,'model_type':model.model_type})
        return out
    except Exception as e:
        print(e)
        return "failed"

def addUserModel(email,model_type,model_name):
    try:
        model = Model(email,model_type,model_name)
        session.add(model)
        session.commit()
    except:
        print(e)
        return "failed"




