from .LinearRegressionController import LinearRegressionController
from .LogisticRegressionController import LogisticRegressionController
from .SVMController import SVMController
from .DecisionTreeController import DecisionTreeController
from .ClusteringController import ClusteringController
from .NaiveBayesController import NaiveBayesController

def MainController(app, request):
    
    @app.route('/')
    def Hello():
        return 'hello'

    @app.route('/linreg',methods=['POST'])
    def linreg():
        return LinearRegressionController(request=request)
    
    @app.route('/logreg',methods=['POST'])
    def logreg():
        return LogisticRegressionController(request=request)
    
    @app.route('/svm',methods=['POST'])
    def svm():
        return SVMController(request=request)
    
    @app.route('/decisiontree',methods=['POST'])
    def decisionTree():
        return DecisionTreeController(request)
    
    @app.route('/clustering',methods=['POST'])
    def clustering():
        return ClusteringController(request)

    @app.route('/naivebayes',methods=['POST'])
    def naiveBayes():
        return NaiveBayesController(request)
    
    
