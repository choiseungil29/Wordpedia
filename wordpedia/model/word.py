from sqlalchemy.dialects import postgresql

from wordpedia import db

class Word(db.Model):

	id = db.Column(db.String(), primary_key=True)
	refCount = db.Column(postgresql.JSON)

	def __init__(self, originalWord):
		self.id = originalWord
		self.refCount = {}

	def __repr__(self):
		return '<id {}>'.format(self.id)