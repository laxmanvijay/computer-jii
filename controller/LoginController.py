def LoginController(request, db):
    email = request.form['email']
    password = request.form['password']
    return db.login(email, password)
