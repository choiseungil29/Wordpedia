import os

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://clogic:tmddlf12@localhost/wordpedia"
db = SQLAlchemy(app)

from wordpedia.model.word import Word
from wordpedia.model.user import User
from wordpedia.model.collection import Collection

db.create_all()
session = db.session

from wordpedia import urls