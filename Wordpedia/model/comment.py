#-*- coding: utf-8 -*-

from sqlalchemy.dialects import postgresql

from wordpedia import db

class Comment(db.Model):
	__tablename__ = 'comment'

	id = db.Column(db.Integer, primary_key=True)
	contents = db.Column(db.String())
	word_id = db.Column(db.String(), db.ForeignKey('word.id'))
	collection_id = db.Column(db.Integer, db.ForeignKey('collection.id'))