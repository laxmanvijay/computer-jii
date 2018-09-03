def CreateUserController(request,db):
    user_name = request.form['user_name']
    email = request.form['email']
    password = request.form['password']
    mobile = request.form['mobile']
    designation = request.form['designation']
    location = request.form['location']
    role = 'user'
    confirmed = False
    return db.createUser(user_name,email,password,mobile,location,designation,role,confirmed)
    #return ("True")
    #except Exception as e:
    #    print(e)
    #    return ("False")
