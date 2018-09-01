def FrontEndController(app, request, db, render_template, session):
    
    @app.route('/')
    def Hello():
        if not session.get('authenticated'):
            return render_template('index.html',user_name=None)
        return render_template('index.html',user_name=session['user_name'])
    
    @app.route('/linreg_page')
    def Linreg():
        if not session.get('authenticated'):
            return render_template('login.html')
        return render_template('linreg.html')

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

    @app.route('/dashboard_page')
    def dashboard_page():
        if not session.get('authenticated'):
            return render_template('login.html')
        return render_template('dashboard.html',user_name=session['user_name'],count=1,email=session['email'],hostname='localhost:5000',models=db.getUserModel(session['email']))
    
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html')
    
    @app.errorhandler(405)
    def page_not_found(e):
        return render_template('404.html')
    
    @app.errorhandler(500)
    def page_not_found(e):
        return render_template('404.html')