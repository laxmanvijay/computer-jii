from flask import Flask,request
from controller import MainController
from database_connector.connector import connect

app = Flask(__name__)

db = connect()

MainController.MainController(app, request)

app.run('localhost')
