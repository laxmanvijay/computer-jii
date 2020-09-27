from flask import Flask,request,render_template,redirect,session
from controller import MainController
from database_connector import dao
import smtplib

app = Flask(__name__,static_url_path='')

smtpObj = smtplib.SMTP('smtp.gmail.com',587)
smtpObj.starttls()
smtpObj.login('<EMAIL>','<PASSWORD>')

MainController.MainController(app, request, dao, render_template,redirect,session,smtpObj)

UPLOAD_FOLDER = 'datasets'
app.secret_key = '<SECRET>'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if __name__=='__main__':
    app.run('localhost',debug=True)
