
import os
import binascii

from sqlalchemy.dialects import postgresql

from wordpedia import db

class User(db.Model):
	__tablename__ = 'user'

	id = db.Column(db.String(), primary_key=True)
	pw = db.Column(db.String())
	token = db.Column(db.String(), unique=True)
	collections = db.Column(postgresql.ARRAY(postgresql.INTEGER))

	def __init__(self, id, password):
		self.id = id
		self.pw = password
		self.token = str(binascii.hexlify(os.urandom(12)))

	def __repr__(self):
		return '<id {}>'.format(self.id)