def CreateUserController(request,db):
    user_name = request.form['user_name']
    email = request.form['email']
    password = request.form['password']
    return db.createUser(user_name,email,password)
    #return ("True")
    #except Exception as e:
    #    print(e)
    #    return ("False")
