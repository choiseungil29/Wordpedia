
import os

from sqlalchemy.dialects import postgresql

from wordpedia import db
from wordpedia.model.user import User

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

	creator = db.Column(db.String)
	creator_token = db.Column(db.String)


	def __init__(self):
		self.words = []
		self.translatedWords = []
		self.fromLanguage = []
		self.refCount = 0
		self.comments = []
		title = None

	def __repr__(self):
		return '<id {}>'.format(self.id)

	def addToUser(token):
		user = db.session.query(User).filter_by(token=token).first()
		user.collections.append(self)
		db.session.flush()

	def getCollection():
		result = {}
		result['id'] = self.id
		result['refs'] = self.refCount
		result['from'] = self.fromLanguage
		result['to'] = self.toLanguage
		result['words'] = self.words
		result['translatedWords'] = self.translatedWords
		result['createDate'] = self.createDate.strftime('%Y/%m/%d')
		result['title'] = self.title
		result['creatorToken'] = self.creator_token
		result['creator'] = self.creator
		result['comments'] = []
		for comment in self.comments.all():
			item = {}
			item['comment'] = comment.contents
			item['creator'] = comment.creator
			item['createDate'] = comment.createDate.strftime('%Y/%m/%d')
			result['comments'].append(item)
		return result









		