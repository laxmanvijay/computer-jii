from .LinearRegressionController import LinearRegressionController
from .LogisticRegressionController import LogisticRegressionController
from .SVMController import SVMController
from .DecisionTreeController import DecisionTreeController
from .ClusteringController import ClusteringController
from .NaiveBayesController import NaiveBayesController
from .CreateUserController import CreateUserController
from .LoginController import LoginController

def MainController(app, request, db):
    
    @app.route('/')
    def Hello():
        return 'hello'

    @app.route('/createuser',methods=['POST'])
    def createUser():
        return CreateUserController(request=request,db=db)

    @app.route('/login',methods=['POST'])
    def login():
        return LoginController(request=request,db=db)

    @app.route('/linreg',methods=['POST'])
    def linreg():
        if LoginController(request=request,db=db)=="password match":
            return LinearRegressionController(request=request,db=db)
        else:
            return "login first"
    
    @app.route('/logreg',methods=['POST'])
    def logreg():
        if LoginController(request=request,db=db)=="password match":
            return LogisticRegressionController(request=request,db=db)
        else:
            return "login first"
    
    @app.route('/svm',methods=['POST'])
    def svm():
        if LoginController(request=request,db=db)=="password match":
            return SVMController(request=request,db=db)
        else:
            return "login first"
    
    @app.route('/decisiontree',methods=['POST'])
    def decisionTree():
        if LoginController(request=request,db=db)=="password match":
            return DecisionTreeController(request=request,db=db)
        else:
            return "login first"
    
    @app.route('/clustering',methods=['POST'])
    def clustering():
        if LoginController(request=request,db=db)=="password match":
            return ClusteringController(request=request,db=db)
        else:
            return "login first"

    @app.route('/naivebayes',methods=['POST'])
    def naiveBayes():
        if LoginController(request=request,db=db)=="password match":
            return NaiveBayesController(request=request,db=db)
        else:
            return "login first"
    
    
