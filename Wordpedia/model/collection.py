
import os

from sqlalchemy.dialects import postgresql

from wordpedia import db

import datetime

class Collection(db.Model):
	__tablename__ = 'collection'

	id = db.Column(db.Integer, primary_key=True)
	words = db.Column(postgresql.ARRAY(postgresql.TEXT))
	translatedWords = db.Column(postgresql.ARRAY(postgresql.TEXT))
	refCount = db.Column(db.Integer)
	fromLanguage = db.Column(postgresql.ARRAY(postgresql.TEXT))
	toLanguage = db.Column(db.String)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	comments = db.relationship('Comment', backref='collection', lazy='dynamic')

	createDate = db.Column(db.DateTime, default=datetime.datetime.utcnow)
	title = db.Column(db.String)


	def __init__(self):
		self.words = []
		self.translatedWords = []
		self.fromLanguage = []
		self.refCount = 0
		self.comments = []
		createDate = db.func.now()
		title = None

	def __repr__(self):
		return '<id {}>'.format(self.id)