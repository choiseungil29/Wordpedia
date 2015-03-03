from Wordpedia import db

class User(db.Model):
	__tablename__ = 'user'

	id = db.Column(db.String(), primary_key=True)
	password = db.Column(db.String())

	def __init__(self, id, password):
		self.id = id
		self.pw = password

	def __repr__(self):
		return '<id {}>'.format(self.id)