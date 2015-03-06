
import os

from sqlalchemy.dialects import postgresql

from wordpedia import db

class Collection(db.Model):
	__tablename__ = 'collection'

	id = db.Column(db.Integer, primary_key=True)
	words = db.Column(postgresql.ARRAY(postgresql.INTEGER))

	def __init__(self):
		pass

	def __repr__(self):
		return '<id {}>'.format(self.id)