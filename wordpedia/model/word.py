from sqlalchemy.dialects import postgresql

from wordpedia import db

class Word(db.Model):

	id = db.Column(db.String(), primary_key=True)
	refCount = db.Column(postgresql.JSON)
	comments = db.relationship('Comment', backref='word', lazy='dynamic')

	def __init__(self, originalWord):
		self.id = unicode(originalWord)
		self.refCount = {}
		self.comments = []

	def __repr__(self):
		return '<id {}>'.format(self.id)