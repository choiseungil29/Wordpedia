
import os

from sqlalchemy.dialects import postgresql

from wordpedia import db

class Collection(db.Model):
	__tablename__ = 'collection'

	id = db.Column(db.Integer, primary_key=True)
	words = db.Column(postgresql.ARRAY(postgresql.TEXT))
	translatedWords = db.Column(postgresql.ARRAY(postgresql.TEXT))
	refCount = db.Column(db.Integer)
	fromLanguage = db.Column(postgresql.ARRAY(postgresql.TEXT))
	toLanguage = db.Column(db.String)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	def __init__(self):
		self.words = []
		self.translatedWords = []
		self.fromLanguage = []
		self.refCount = 0

	def __repr__(self):
		return '<id {}>'.format(self.id)