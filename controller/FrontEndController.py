def FrontEndController(app, request, db, render_template, session):
    
    @app.route('/')
    def Hello():
        if not session.get('authenticated'):
            return render_template('index.html',user_name=None)
        return render_template('index.html',user_name=session['user_name'])

    @app.route('/login_page')
    def Login_page():
        if request.args['error']=='true':
            return render_template('login.html',error='error')
        return render_template('login.html')
    
    @app.route('/register_page')
    def Register_page():
        return render_template('register.html')

    @app.route('/dashboard_page')
    def dashboard_page():
        return render_template('dashboard.html',user_name=session['user_name'],models=db.getUserModel(session['email']))