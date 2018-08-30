from .LinearRegressionController import LinearRegressionController
from .LogisticRegressionController import LogisticRegressionController
from .SVMController import SVMController
from .DecisionTreeController import DecisionTreeController
from .ClusteringController import ClusteringController
from .NaiveBayesController import NaiveBayesController
from .CreateUserController import CreateUserController
from .LoginController import LoginController
from .FrontEndController import FrontEndController


def MainController(app, request, db, render_template, redirect, session):

    # front end routes
    FrontEndController(app, request, db, render_template, session)
    
    ###
    # back end routes
    ###

    @app.route('/createuser', methods=['POST'])
    def createUser():
        res = CreateUserController(request=request, db=db)
        if res=='ok':
            session['authenticated']=True
            session['user_name'] = request.form['user_name']
            session['email'] = request.form['email']
            return redirect('/')
        else:
            return redirect('/login_page?error=user_exist')

    @app.route('/login', methods=['POST'])
    def login():
        res=LoginController(request=request, db=db)
        if res=='password match':
            session['authenticated']=True
            session['user_name'] = db.getUserNameByEmail(request.form['email'])
            session['email'] = request.form['email']
            return redirect('/')
        elif res=='user not exist':
            return redirect('/register_page?error=true')
        else:
            return redirect('/login_page?error=true')

    @app.route('/logout')
    def logout():
        session['authenticated']=False
        return redirect('/')

    @app.route('/linreg', methods=['POST'])
    def linreg():
        if session['authenticated']==True:
            if LinearRegressionController(request=request, db=db, session=session)=='Ok model trained':
                return redirect('/dashboard_page')
        else:
            return redirect('login_page?error=False')

    @app.route('/logreg', methods=['POST'])
    def logreg():
        if session['authenticated']==True:
            return LogisticRegressionController(request=request, db=db, session=session)
        else:
            return redirect('login_page?error=False')

    @app.route('/svm', methods=['POST'])
    def svm():
        if session['authenticated']==True:
            return SVMController(request=request, db=db, session=session)
        else:
            return redirect('login_page?error=False')

    @app.route('/decisiontree', methods=['POST'])
    def decisionTree():
        if session['authenticated']==True:
            return DecisionTreeController(request=request, db=db, session=session)
        else:
            return redirect('login_page?error=False')

    @app.route('/clustering', methods=['POST'])
    def clustering():
        if session['authenticated']==True:
            return ClusteringController(request=request, db=db, session=session)
        else:
            return redirect('login_page?error=False')

    @app.route('/naivebayes', methods=['POST'])
    def naiveBayes():
        if session['authenticated']==True:
            return NaiveBayesController(request=request, db=db, session=session)
        else:
            return redirect('login_page?error=False')
    
    @app.route('/user/<username>/<model_type>/<model_name>')
    def getModel(username,model_type,model_name):
        if session['authenticated']==True:
            return ''+username+model_type+model_name
        else:
            return redirect('login_page?error=False')
