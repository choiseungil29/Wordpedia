#-*- coding: utf-8 -*-

from flask import request, Response

from sqlalchemy.orm.exc import NoResultFound

from microsofttranslator import Translator

from wordpedia import app
from wordpedia import session

from wordpedia.model.collection import Collection
from wordpedia.model.word import Word
from wordpedia.model.user import User
from wordpedia.model.comment import Comment

import json

@app.route('/comment/add', methods=['POST', 'GET'])
def add():
	targetWord = request.args['targetWord']
	targetCollectionId = request.args['targetCollectionId']
	content = request.args['comment']

	try:
		session.query(Word).filter_by(id=targetWord).one()
		session.query(Collection).filter_by(id=targetCollectionId).one()
	except:
		return 'failed'

	comment = Comment()
	comment.contents = content
	comment.collection_id = targetCollectionId
	comment.word_id = targetWord

	"""word = session.query(Word).filter_by(id=targetWord).first()
	if word is None:
		return 'failed'
	word.comments.append(comment.id)

	collection = session.query(Collection).filter_by(id=targetCollectionId).first()
	if collection is None:
		return 'failed'
	collection.comments.append(comment.id)"""
	
	session.add(comment)
	session.commit()

	return json.dumps(comment.contents, ensure_ascii=False)