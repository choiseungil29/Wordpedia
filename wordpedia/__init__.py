import os

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://clogic:tmddlf12@localhost/wordpedia"
db = SQLAlchemy(app)

from wordpedia import urls
