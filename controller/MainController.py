from .LinearRegressionController import LinearRegressionController
from .LogisticRegressionController import LogisticRegressionController
from .SVMController import SVMController
from .DecisionTreeController import DecisionTreeController
from .ClusteringController import ClusteringController
from .NaiveBayesController import NaiveBayesController
from .CreateUserController import CreateUserController
from .LoginController import LoginController
from .FrontEndController import FrontEndController
from .AdminController import AddTrainableModelController, AddNonTrainableModelController
import os
from werkzeug.utils import secure_filename
from flask import send_from_directory
from pathlib import Path
from itsdangerous import URLSafeTimedSerializer
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def MainController(app, request, db, render_template, redirect, session,smtpObj):

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
            session['confirmed'] = False
            confirm_serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

            token=confirm_serializer.dumps(session.get('email'), salt='email-confirmation-salt')
            confirm_url = 'http://localhost:5000/confirm_email?token=%s'%(token)
            html = render_template('confirmation_email_template.html',confirm_url=confirm_url)
            subject='confirm your computer jii account.'
            send_mail(session['email'],subject,html)
            return redirect('/')
        else:
            return redirect('/login_page?error=user_exist')
    
    @app.route('/resend_confirmation')
    def resend_confirmation():
        confirm_serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

        token=confirm_serializer.dumps(session.get('email'), salt='email-confirmation-salt')
        confirm_url = 'http://localhost:5000/confirm_email?token=%s'%(token)
        html = render_template('confirmation_email_template.html',confirm_url=confirm_url)
        subject='confirm your computer jii account.'
        send_mail(session['email'],subject,html)
        return redirect('/')

    @app.route('/confirm_email')
    def confirm_mail():
        confirm_serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        token = request.args['token']
        email = confirm_serializer.loads(token, salt='email-confirmation-salt', max_age=3600)
        db.updateConfirmation(email)
        return redirect('/login_page?error=false')

    def send_mail(email,subject,html):
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = 'laxmanvijay24@gmail.com'
        msg['To'] = email
        part2 = MIMEText(html, 'html')
        msg.attach(part2)
        smtpObj.sendmail("laxmanvijay24@gmail.com", email, msg.as_string()) 
        return

    @app.route('/verifyemailpassword',methods=['POST'])
    def verifyEmailPassword():
        email = request.form['email']
        confirm_serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

        token=confirm_serializer.dumps(email, salt='email-confirmation-salt')
        confirm_url = 'http://localhost:5000/updatepassword_page?token=%s'%(token)
        html = render_template('confirmation_email_password_template.html',confirm_url=confirm_url)
        subject = 'change password for computer jii account.'
        send_mail(email,subject, html)
        
        return redirect('/')


    @app.route("/updatepassword",methods=['POST'])
    def updatePassword():
        email = request.form['email']
        password = request.form['password']
        if db.updatePassword(email,password)=='user not confirmed':
            return redirect('/dashboard_page')
        else:
            return redirect('/login_page?error=false')


    @app.route('/login', methods=['POST'])
    def login():
        res=LoginController(request=request, db=db)
        if res=='password confirmed':
            session['authenticated']=True
            session['user_name'] = db.getUserNameByEmail(request.form['email'])
            session['email'] = request.form['email']
            session['role'] = 'user'
            session['confirmed']=True
            return redirect('/')
        elif res=='password match':
            session['authenticated']=True
            session['user_name'] = db.getUserNameByEmail(request.form['email'])
            session['email'] = request.form['email']
            session['role'] = 'user'
            session['confirmed']=False
            return redirect('/')
        elif res=='password admin':
            session['authenticated']=True
            session['user_name'] = db.getUserNameByEmail(request.form['email'])
            session['email'] = request.form['email']
            session['role'] = 'admin'
            session['confirmed']=True
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
                db.addUserModel(session.get('email'),'svm',request.form['model_name'])
                db.setModelApi(session.get('email'),request.form['model_type'],request.form['model_name'],generateApi(session.get('email'),request.form['model_type'],request.form['model_name']))
                db.setModelUserRequestDetails(session.get('email'),request.form['model_type'],request.form['model_name'],0)
                db.incrementModelUserCount(session.get('email'),request.form['model_type'])
                db.incrementModelCount(request.form['model_type'])
                return redirect('/dashboard_page')
        else:
            return redirect('login_page?error=False')

    @app.route('/logreg', methods=['POST'])
    def logreg():
        if session['authenticated']==True:
            if LogisticRegressionController(request=request, db=db, session=session)=='Ok model trained':
                db.addUserModel(session.get('email'),'svm',request.form['model_name'])
                db.setModelApi(session.get('email'),request.form['model_type'],request.form['model_name'],generateApi(session.get('email'),request.form['model_type'],request.form['model_name']))
                db.setModelUserRequestDetails(session.get('email'),request.form['model_type'],request.form['model_name'],0)
                db.incrementModelUserCount(session.get('email'),request.form['model_type'])
                db.incrementModelCount(request.form['model_type'])
                return redirect('/dashboard_page')
        else:
            return redirect('login_page?error=False')

    @app.route('/svm', methods=['POST'])
    def svm():
        if session['authenticated']==True:
            if SVMController(request=request, db=db, session=session)=='Ok model trained':
                db.addUserModel(session.get('email'),'svm',request.form['model_name'])
                db.setModelApi(session.get('email'),request.form['model_type'],request.form['model_name'],generateApi(session.get('email'),request.form['model_type'],request.form['model_name']))
                db.setModelUserRequestDetails(session.get('email'),request.form['model_type'],request.form['model_name'],0)
                db.incrementModelUserCount(session.get('email'),request.form['model_type'])
                db.incrementModelCount(request.form['model_type'])
                return redirect('/dashboard_page')
        else:
            return redirect('login_page?error=False')

    @app.route('/decisiontree', methods=['POST'])
    def decisionTree():
        if session['authenticated']==True:
            if DecisionTreeController(request=request, db=db, session=session)=='Ok model trained':
                db.addUserModel(session.get('email'),'svm',request.form['model_name'])
                db.setModelApi(session.get('email'),request.form['model_type'],request.form['model_name'],generateApi(session.get('email'),request.form['model_type'],request.form['model_name']))
                db.setModelUserRequestDetails(session.get('email'),request.form['model_type'],request.form['model_name'],0)
                db.incrementModelUserCount(session.get('email'),request.form['model_type'])
                db.incrementModelCount(request.form['model_type'])
                return redirect('/dashboard_page')
        else:
            return redirect('login_page?error=False')

    @app.route('/clustering', methods=['POST'])
    def clustering():
        if session['authenticated']==True:
            if ClusteringController(request=request, db=db, session=session)=='Ok model trained':
                db.addUserModel(session.get('email'),'svm',request.form['model_name'])
                db.setModelApi(session.get('email'),request.form['model_type'],request.form['model_name'],generateApi(session.get('email'),request.form['model_type'],request.form['model_name']))
                db.setModelUserRequestDetails(session.get('email'),request.form['model_type'],request.form['model_name'],0)
                db.incrementModelUserCount(session.get('email'),request.form['model_type'])
                db.incrementModelCount(request.form['model_type'])
                return redirect('/dashboard_page')
        else:
            return redirect('login_page?error=False')

    @app.route('/naivebayes', methods=['POST'])
    def naiveBayes():
        if session['authenticated']==True:
            if NaiveBayesController(request=request, db=db, session=session)=='Ok model trained':
                db.addUserModel(session.get('email'),'svm',request.form['model_name'])
                db.setModelApi(session.get('email'),request.form['model_type'],request.form['model_name'],generateApi(session.get('email'),request.form['model_type'],request.form['model_name']))
                db.setModelUserRequestDetails(session.get('email'),request.form['model_type'],request.form['model_name'],0)
                db.incrementModelUserCount(session.get('email'),request.form['model_type'])
                db.incrementModelCount(request.form['model_type'])
                return redirect('/dashboard_page')
        else:
            return redirect('login_page?error=False')

    @app.route('/addtrainablemodel',methods=['POST'])
    def addTrainableModel():
        if session['authenticated']==True:
            if session['role']=='admin':
                if AddTrainableModelController(request=request, db=db, session=session)=="ok":
                    return redirect('/admin_dashboard')
            else:
                return redirect('/')
        else:
            return redirect('/login_page?error=False')
    
    @app.route('/addnontrainablemodel',methods=['POST'])
    def addNonTrainableModel():
        if session['authenticated']==True:
            if session['role']=='admin':
                if AddNonTrainableModelController(request=request, db=db, session=session)=="ok":
                    return redirect('/admin_dashboard')
            else:
                return redirect('/')
        else:
            return redirect('/login_page?error=False')
    
    @app.route('/adddataset',methods=['POST'])
    def addDataset():
        dataset = request.files['data']
        #basedir = os.path.abspath(os.path.dirname(__file__))
        f=os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(session.get('email')+"_"+dataset.filename))
        sf=f
        dataset.save(sf)
        # with open(sf,'wb') as f:
        #     f.write(dataset)
        size_val = os.stat(f).st_size
        host='localhost:5000'
        api_url = 'http://%s/dataset?email=%s&dataset_name=%s'%(host,session.get('email'),secure_filename(session.get('email')+"_"+dataset.filename))
        db.addDataset(session.get('email'),secure_filename(session.get('email')+"_"+dataset.filename),api_url,size_val)
        return redirect('/dashboard_page')

    @app.route('/dataset')
    def getDataset():
        return send_from_directory(app.config['UPLOAD_FOLDER'],request.args['dataset_name'])

    @app.route('/deletedataset',methods=['POST'])
    def deleteDataset():
        email = request.form['email']
        name = request.form['name']
        os.remove('datasets/%s'%(name))
        db.deleteDataset(name,email)
        return redirect('/dashboard_page')

    @app.route('/predict',methods=['POST'])
    def getModel():
        x=request.args['model_type']
        if x=='linreg':
            return LinearRegressionController(request,db,session)

    def generateApi(email,model_type,name):
        host = 'localhost:5000'
        return 'http://%s/predict?email=%s&model_type=%s&model_name=%s' % (host,email,model_type,name)