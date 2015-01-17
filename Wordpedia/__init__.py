from flask import Flask
from flaskext.mysql import MySQL

#from whisper.urls import app

app = Flask(__name__)
app.debug = True

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'ok154288tmddlf'
app.config['MYSQL_DATABASE_DB'] = 'whisper'

mysql = MySQL()
mysql.init_app(app)