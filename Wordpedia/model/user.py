
import os
import binascii

from sqlalchemy.dialects import postgresql

from wordpedia import db

class User(db.Model):
	__tablename__ = 'user'

	userId = db.Column(db.String())
	id = db.Column(db.Integer, primary_key=True)
	pw = db.Column(db.String())
	token = db.Column(db.String(), unique=True)
	collections = db.relationship('Collection', backref='user', lazy='dynamic')

	def __init__(self, id, password):
		self.userId = id
		self.pw = password
		self.token = str(binascii.hexlify(os.urandom(12)))
		self.collections = []

	def __repr__(self):
		return '<id {}>'.format(self.id)

	def tokenCheck(token):
		try:
			session.query(User).filter_by(token=token).one()
		except:
			raise ValueError