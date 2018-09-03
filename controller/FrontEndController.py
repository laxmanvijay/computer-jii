from itsdangerous import URLSafeTimedSerializer

def FrontEndController(app, request, db, render_template, session):
    
    @app.route('/')
    def Hello():
        if not session.get('authenticated'):
            return render_template('index.html',user_name=None)
        return render_template('index.html',user_name=session['user_name'])
    
    @app.route('/linreg_page')
    def Linreg_page():
        if not session.get('authenticated'):
            return render_template('login.html')
        return render_template('linreg.html')
    
    @app.route('/logreg_page')
    def Logreg_page():
        if not session.get('authenticated'):
            return render_template('login.html')
        return render_template('logreg.html')
    
    @app.route('/svm_page')
    def svm_page():
        if not session.get('authenticated'):
            return render_template('login.html')
        return render_template('svm.html')
    
    @app.route('/decisiontree_page')
    def decisionTree_page():
        if not session.get('authenticated'):
            return render_template('login.html')
        return render_template('decisiontree.html')
    
    @app.route('/clustering_page')
    def clustering_page():
        if not session.get('authenticated'):
            return render_template('login.html')
        return render_template('clustering.html')
    
    @app.route('/naivebayes_page')
    def naiveBayes_page():
        if not session.get('authenticated'):
            return render_template('login.html')
        return render_template('naivebayes.html')

    @app.route('/login_page')
    def Login_page():
        if request.args['error']=='password':
            return render_template('login.html',error='password')
        elif request.args['error']=='user_exist':
            return render_template('login.html',error='user_exist')
        return render_template('login.html')

    @app.route('/register_page')
    def Register_page():
        if request.args['error']=='true':
            return render_template('register.html',error='error')
        return render_template('register.html')
    
    @app.route('/addtrainablemodel_page')
    def addTrainableModel_page():
        if not session.get('authenticated'):
            return render_template('login.html')
        elif not session.get('role')=='admin':
            return render_template('index.html')
        return render_template('addtrainablemodel.html')
    
    @app.route('/addnontrainablemodel_page')
    def addNonTrainableModel_page():
        if not session.get('authenticated'):
            return render_template('login.html')
        elif not session.get('role')=='admin':
            return render_template('404.html')
        return render_template('addnontrainablemodel.html')

    @app.route('/admin_dashboard')
    def adminDashboard_page():
        if not session.get('authenticated'):
            return render_template('login.html')
        elif not session.get('role')=='admin':
            return render_template('404.html')
        return render_template('admin_dashboard.html')

    @app.route('/dashboard_page')
    def dashboard_page():
        if not session.get('authenticated'):
            return render_template('login.html')
        if not session.get('confirmed'):
            return render_template('unconfirmed_dashboard.html')
        user = db.getUserByEmail(session['email'])
        models = db.getModelUserCountDetails(session['email'])
        request_models  = db.getModelUserRequestDetails(session['email'])
        api = db.getModelUserApiDetails(session['email'])
        model_desc = db.getAllTrainableModelDescription()
        datasets = db.getDatasetsByEmail(session['email'])
        return render_template('dashboard.html',user=user,datasets=datasets,model_desc=model_desc,api=api,hostname='localhost:5000',models=models,request=request_models)
    
    @app.route('/updatepassword_page')
    def updatePassword_page():
        confirm_serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        token = request.args['token']
        email = confirm_serializer.loads(token, salt='email-confirmation-salt', max_age=3600)
        return render_template('update_password.html',email=email)

    @app.route('/verifyemailpassword_page')
    def verifyEmailPassword_page():
        return render_template('verifyemailpassword.html')

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html')
    
    @app.errorhandler(405)
    def page_not_found(e):
        return render_template('404.html')
    
    @app.errorhandler(500)
    def page_not_found(e):
        return render_template('404.html')