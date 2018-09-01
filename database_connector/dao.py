from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .db_connector import connector
from .dto import User, Model, Base, ModelApi, ModelCount, ModelRequest, ModelUserCount, TrainableModels, NonTrainableModels

engine = create_engine(connector)

Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)

session = DBSession()

def checkUserExist(email):
    o=[]
    user = session.query(User.email).all()
    for i in user:
        o.append(i[0])# [('laxmanvijay24@gmail.com'),()]
    if email in o:
        return True
    return False

def createUser(name,email,password):
    user_check = checkUserExist(email)
    if not user_check:
        user = User(name,email,password)
        session.add(user)
        session.commit()
        return "ok"
    else:
        return "user exists"
    #except:
    #    print("err")
    #    return "not ok"


def login(email,password):
    user_check = checkUserExist(email)
    if not user_check:
        return "user not exist"
    else:
        user = session.query(User).filter(User.email==email).one()
        if user.password == password:
            return "password match"
        else:
            return "password do not match"

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

def getAllUsers():
    users = session.query(User).all()
    return users

def getAllTrainableModelDescription():
    models = session.query(TrainableModels).all()
    return models

def getAllNonTrainableModelDescription():
    models = session.query(NonTrainableModels).all()
    return models

def getTrainableModelDescription(model_type):
    model_desc = session.query(TrainableModels).filter(TrainableModels.model_type==model_type).one()
    return model_desc

def getNonTrainableModelDescription(model_type):
    model_desc = session.query(NonTrainableModels).filter(NonTrainableModels.model_type==model_type).one()
    return model_desc

def getModelUserCount(email,model_type):
    count = session.query(ModelUserCount.count).filter(ModelUserCount.email==email and ModelUserCount.model_type==model_type).one()
    return count

def incrementModelUserCount(email,model_type):
    session.query(ModelUserCount)\
                .filter(ModelUserCount.email==email and ModelUserCount.model_type==model_type)\
                .update({"count":(ModelUserCount.count+1)})
    session.commit()
    return "ok"

def getModelRequest(email,model_type,model_name):
    count = session.query(ModelRequest.count).filter(ModelRequest.email==email and ModelRequest.model_type==model_type and ModelRequest.model_name==model_name).one()
    return count

def incrementModelUserCount(email,model_type):
    session.query(ModelRequest.count)\
                    .filter(ModelRequest.email==email and ModelRequest.model_type==model_type and ModelRequest.model_name==model_name)\
                    .update({"count":(ModelRequest.count+1)})
    session.commit()
    return "ok"

def getModelCount(model_type):
    count = session.query(ModelCount.count)\
                   .filter(ModelCount.model_type==model_type)\
                   .one()
    return count

def incrementModelCount(model_type):
    session.query(ModelCount)\
                 .filter(ModelCount.model_type==model_type)\
                 .update({"count":(ModelCount.count+1)})
    session.commit()
    return "ok"

def getModelApi(email,model_type,model_name):
    row = session.query(ModelApi)\
                 .filter(ModelApi.model_type==model_type, ModelApi.email==email, ModelApi.model_name==model_name)\
                 .one()
    return row

def setModelApi(email,model_type,model_name):
    row = ModelApi(email,model_type,model_name,api)
    session.add(row)
    session.commit()
    return "ok"
