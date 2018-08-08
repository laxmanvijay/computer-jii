from flask import Flask,request
from controller import MainController

app = Flask(__name__)

MainController.MainController(app, request)

app.run('localhost')
