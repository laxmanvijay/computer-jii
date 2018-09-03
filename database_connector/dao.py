from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .db_connector import connector
from .dto import User, Model, Datasets, Base, ModelApi, ModelCount, ModelRequest, ModelUserCount, TrainableModels, NonTrainableModels
import bcrypt

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

def createUser(name,email,password,mobile,location,designation,role,confirmed):
    user_check = checkUserExist(email)
    if not user_check:
        salt = bcrypt.gensalt()
        password = bcrypt.hashpw(password.encode('utf8'), salt)
        user = User(name,email,password,mobile,location,designation,role,confirmed)
        session.add(user)

        trainablemodels = getAllTrainableModelDescription()
        o = []
        for i in trainablemodels:
            o.append(i.model_type) # 
        
        for i in o:
            m = ModelUserCount(email,i,0)
            session.add(m)

        session.commit()
        return "ok"
    else:
        return "user exists"
    #except:
    #    print("err")
    #    return "not ok"

def updateConfirmation(email):
    user = session.query(User).filter(User.email==email)\
                  .update({'confirmed':True})
    session.commit()
    return "ok"

def updatePassword(email,password):
    user = session.query(User).filter(User.email==email).one()
    if not user.confirmed:
        return 'user not confirmed'
    salt = bcrypt.gensalt()
    password = bcrypt.hashpw(password, salt)
    user.password = password
    session.commit()
    return 'ok'

def login(email,password):
    user_check = checkUserExist(email)
    if not user_check:
        return "user not exist"
    else:
        user = session.query(User).filter(User.email==email).one()
        
        if bcrypt.checkpw(password.encode('utf8'),user.password.encode('utf8')):
            if user.role == 'admin':
                return "password admin"

            if user.confirmed==True:
                return "password confirmed"
            return "password match"
        else:
            return "password do not match"

def getUserNameByEmail(email):
    user = session.query(User).filter(User.email==email).one()
    return user.name

def getUserByEmail(email):
    user = session.query(User).filter(User.email==email).one()
    return user


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

def addTrainableModel(model_type,model_description,input_format,output_format,route_url):
    model = TrainableModels(model_type,model_description,input_format,output_format,route_url)
    session.add(model)

    model2 = ModelCount(model_type,0)
    session.add(model2)

    o=[]
    users = getAllUsers()
    for i in users:
        o.append(i.email)
    
    for i in o:
        m = ModelUserCount(i,model_type,0)
        session.add(m)

    session.commit()
    return 'ok'

def getNonTrainableModelDescription(model_type):
    model_desc = session.query(NonTrainableModels).filter(NonTrainableModels.model_type==model_type).one()
    return model_desc

def addNonTrainableModel(model_type,model_description,input_format,output_format,route_url):
    model = NonTrainableModels(model_type,model_description,input_format,output_format,route_url)
    session.add(model)

    model2 = ModelCount(model_type,0)
    session.add(model2)

    o=[]
    users = getAllUsers()
    for i in user:
        o.append(i.email)
    
    for i in o:
        m = ModelUserCount(i,model_type,0)
        session.add(m)

    session.commit()
    return 'ok'
  

def getModelUserCount(email,model_type):
    count = session.query(ModelUserCount.count).filter(ModelUserCount.email==email and ModelUserCount.model_type==model_type).one()
    return count

def getModelUserCountDetails(email):
    try:
        models = session.query(ModelUserCount).filter(ModelUserCount.email==email).all()
        out = []
        for model in models:
            out.append({'model_type':model.model_type,'count':model.count})
        return out
    except Exception as e:
        print(e)
        return "failed"

def incrementModelUserCount(email,model_type):
    session.query(ModelUserCount)\
                .filter(ModelUserCount.email==email, ModelUserCount.model_type==model_type)\
                .update({"count":(ModelUserCount.count+1)})
    session.commit()
    return "ok"

def getModelRequest(email,model_type,model_name):
    count = session.query(ModelRequest.request).filter(ModelRequest.email==email, ModelRequest.model_type==model_type and ModelRequest.model_name==model_name).one()
    return count

def getModelUserRequestDetails(email):
    try:
        models = session.query(ModelRequest).filter(ModelRequest.email==email).all()
        out = []
        for model in models:
            out.append({'model_name':model.model_name,'model_type':model.model_type,'count':model.request})
        return out
    except Exception as e:
        print(e)
        return "failed"

def setModelUserRequestDetails(email,model_type,model_name,request):
    model = ModelRequest(email,model_type,model_name,request)
    session.add(model)
    session.commit()
    return 'ok'

def incrementModelUserRequestCount(email,model_type):
    session.query(ModelRequest.count)\
                    .filter(ModelRequest.email==email, ModelRequest.model_type==model_type, ModelRequest.model_name==model_name)\
                    .update({"request":(ModelRequest.request+1)})
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

def getModelUserApiDetails(email):
    try:
        models = session.query(ModelApi).filter(ModelApi.email==email).all()
        out = []
        for model in models:
            out.append({'model_name':model.model_name,'model_type':model.model_type,'api':model.api})
        return out
    except Exception as e:
        print(e)
        return "failed"

def setModelApi(email,model_type,model_name,api):
    row = ModelApi(email,model_type,model_name,api)
    session.add(row)
    session.commit()
    return "ok"

def getAllDatasets():
    datasets = session.query(Datasets).all()
    return datasets

def getDatasetsByEmail(email):
    datasets = session.query(Datasets).filter(Datasets.email == email).all()
    return datasets

def addDataset(email,dataset_name,api_url,dataset_size):
    dataset = Datasets(email,dataset_name,api_url,dataset_size)
    session.add(dataset)
    session.commit()
    return "ok"
def deleteDataset(name,email):
    session.query(Datasets)\
           .filter(Datasets.email==email,Datasets.dataset_name==name)\
           .delete(synchronize_session=False)
    session.commit()
    return "ok"
