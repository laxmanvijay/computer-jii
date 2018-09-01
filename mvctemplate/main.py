from flask import Flask,request,render_template,redirect,session
from controller import MainController
from dbcontroller import dao

app = Flask(__name__,static_url_path='')


MainController.MainController(app, request, dao, render_template,redirect,session)

app.secret_key = '12344sefsrfsrg'
if __name__=='__main__':
    app.run('localhost',debug=True)
