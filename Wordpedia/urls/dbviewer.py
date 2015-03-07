#-*- coding: utf-8 -*-

from flask import request

from sqlalchemy.orm.exc import NoResultFound

from wordpedia import app
from wordpedia import session

from wordpedia.model.word import Word
from wordpedia.model.user import User
from wordpedia.model.collection import Collection

import json

@app.route('/view/db/word', methods=['GET', 'POST'])
def word():
	result = {}

	try:
		word = session.query(Word).filter(Word.id == request.args.get('w')).one()
	except NoResultFound, e:
		return '존재하지 않는 단어입니다.'

	result['id'] = word.id
	result['refCount'] = json.loads(str(word.refCount))

	return json.dumps(result, ensure_ascii=False)

@app.route('/view/db/word/all')
def words():
	result = []
	for word in session.query(Word).all():
		item = {}
		item['word'] = word.id
		item['refs'] = json.loads(word.refCount)
		result.append(item)

	return json.dumps(result, ensure_ascii=False)

@app.route('/view/db/collection/all')
def collections():
	result = []

	for collection in session.query(Collection).all():
		item = {}
		item['id'] = collection.id
		item['refs'] = collection.refCount
		item['from'] = collection.fromLanguage
		item['to'] = collection.toLanguage
		item['words'] = collection.words
		item['translatedWords'] = collection.translatedWords
		result.append(item)

	return json.dumps(result, ensure_ascii=False)

@app.route('/view/user/info')
def userInfo():
	id = request.args.get('id')
	result = {}

	user = session.query(User).filter_by(id=id).first()
	if user is None:
		return 'invalid id'

	result['id'] = user.id
	result['token'] = user.token

	return json.dumps(result)

@app.route('/view/user/collections')
def collectionsOfUser():
	id = request.args.get('id')
	result = {}

	user = session.query(User).filter_by(userId=id).first()
	if user is None:
		return

	result['id'] = user.id
	result['token'] = user.token
	result['collections'] = []
	for collection in user.collections.all():
		item = {}
		item['id'] = collection.id
		item['refs'] = collection.refCount
		item['from'] = collection.fromLanguage
		item['to'] = collection.toLanguage
		item['words'] = collection.words
		item['translatedWords'] = collection.translatedWords
		result['collections'].append(item)

	return json.dumps(result, ensure_ascii=False)



























