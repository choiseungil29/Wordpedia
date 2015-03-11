#-*- coding: utf-8 -*-

from flask import request

from sqlalchemy.orm.exc import NoResultFound

from wordpedia import app
from wordpedia import session

from wordpedia.model.word import Word
from wordpedia.model.user import User
from wordpedia.model.comment import Comment
from wordpedia.model.collection import Collection

import json

@app.route('/get/collection', methods=['POST', 'GET'])
def collection():
	id = request.args['collectionId']

	collection = session.query(Collection).filter_by(id=id).first()
	if collection is None:
		return '존재하지 않는 단어장입니다'

	resumt = setCollection(collection)

	return json.dumps(result, ensure_ascii=False)

@app.route('/get/collection/all', methods=['POST', 'GET'])
def collections():
	result = []

	for collection in session.query(Collection).all():
		item = setCollection(collection)
		result.append(item)

	return json.dumps(result, ensure_ascii=False)

@app.route('/get/collection/user', methods=['POST', 'GET'])
def collectionsOfUser():
	token = request.headers['token']
	result = {}

	user = session.query(User).filter_by(token=token).first()
	if user is None:
		return '존재하지 않는 유저입니다'

	result['id'] = user.id
	result['userId'] = user.userId
	result['token'] = user.token
	result['collections'] = []
	for collection in user.collections.all():
		item = setCollection(collection)
		result['collections'].append(item)

	return json.dumps(result, ensure_ascii=False)

def setCollection(collection):
	result = {}
	result['id'] = collection.id
	result['refs'] = collection.refCount
	result['from'] = collection.fromLanguage
	result['to'] = collection.toLanguage
	result['words'] = collection.words
	result['translatedWords'] = collection.translatedWords
	result['createDate'] = collection.createDate.strftime('%Y/%m/%d')
	result['title'] = collection.title
	result['creatorToken'] = collection.creator_token
	result['creator'] = collection.creator
	result['comments'] = []
	for comment in collection.comments.all():
		item = {}
		item['comment'] = comment.contents
		item['creator'] = comment.creator
		item['createDate'] = comment.createDate.strftime('%Y/%m/%d')
		result['comments'].append(item)
	return result


























