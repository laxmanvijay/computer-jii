from flask import Flask,request
from controller import MainController
from database_connector import dao

app = Flask(__name__)


MainController.MainController(app, request, dao)

app.run('localhost')
