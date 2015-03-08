import os

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://clogic:tmddlf12@localhost/wordpedia"
#app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://fliapubcocxlhn:a5a8YjMKgeHEOFq8RHoBMUU6uC@ec2-107-20-244-39.compute-1.amazonaws.com:5432/daj8pkrf41q6hr"
db = SQLAlchemy(app)

from wordpedia.model.comment import Comment
from wordpedia.model.word import Word
from wordpedia.model.user import User
from wordpedia.model.collection import Collection

db.create_all()
session = db.session

from wordpedia import urls