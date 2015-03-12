#-*- coding: utf-8 -*-

from flask import request, Response

from sqlalchemy.orm.exc import NoResultFound

from microsofttranslator import Translator

from wordpedia import app
from wordpedia import session

from wordpedia.model.collection import Collection
from wordpedia.model.word import Word
from wordpedia.model.user import User

import json

from wordpedia.random import Random

t = Translator('Wordpedia', 'f1wB2fFCQMVoKPTFqPxMwO79Qxg816xYE7Y5eNF4lBk=')

@app.route('/collection/create', methods=['GET', 'POST'])
def create():
	"""
	params:
	requst
	 w : word list.
	 to : language code that want to return
	headers
	 token : user token
	"""
	
	if request.args['title'] is None:
			return '타이틀이 존재하지 않습니다'
			
	try:
		token = request.headers.get('token')
		collection = createCollection(request.values.getlist('w'), request.args['to'], request.args['title'], token)
		collection.addToUser(token)
	except ValueError, e:
		return 'error. failed create collection'
	except:
		return token
	session.commit()

	result = {}
	result['requestCode'] = 1
	result['requestMessage'] = '단어장 생성에 성공하였습니다.'
	result['collectionId'] = collection.id

	return json.dumps(result, ensure_ascii=False)

@app.route('/collection/copy', methods=['POST', 'GET'])
def copy():
	"""
	다른 유저에게 collection id값을 복사해준다.
	"""

	collectionId = request.args['collectionId']
	token = request.headers.get('token')

	user = session.query(User).filter_by(token=token).first()
	if user is None:
		return '존재하지 않는 user입니다'

	collection = session.query(Collection).filter_by(id=collectionId).first()
	if collection is None:
		return '단어장이 존재하지 않습니다'

	result = {}
	result['requestCode'] = 1
	result['requestMessage'] = '복사에 성공했습니다.'
	result['collectionId'] = collection.id

	collection.addToUser(token)
	return json.dumps(result, ensure_ascii=False)

@app.route('/get/collection', methods=['POST', 'GET'])
def collection():
	id = request.args['collectionId']

	collection = session.query(Collection).filter_by(id=id).first()
	if collection is None:
		return '존재하지 않는 단어장입니다'

	result = collection.getCollection()

	return json.dumps(result, ensure_ascii=False)

@app.route('/get/collection/all', methods=['POST', 'GET'])
def collections():
	result = []

	for collection in session.query(Collection).all():
		item = collection.getCollection()
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
		item = collection.getCollection()
		result['collections'].append(item)

	return json.dumps(result, ensure_ascii=False)

@app.route('/surf', methods=['POST', 'GET'])
def surf():
	token = request.headers['token']

	result = []
	for collection in session.query(Collection).all():
		if collection.creator_token is token:
			continue

		result.append(collection)

	random = Random()
	target = random.randrange(0, len(result))
	#target = len(result) - 2

	return json.dumps(result[target].getCollection(), ensure_ascii=False)

def createCollection(words, toLanguage, title, token):
	result = {}
	collection = Collection()

	collection.title = title

	data = t.translate_array(words, toLanguage)
	for i in range(0, len(words)):

		word = session.query(Word).filter(Word.id == words[i]).first()
		if word is None:
			word = Word(words[i]) # json데이터 집어넣어야
			session.add(word)
			session.flush()

		refs = json.loads(str(word.refCount))
		if data[i]['From'] not in refs:
			refs[data[i]['From']] = 0
		refs[data[i]['From']] += 1
		word.refCount = json.dumps(refs)

		result[word.id] = {}
		result[word.id]['translatedText'] = data[i]['TranslatedText']
		result[word.id]['refCount'] = refs
		session.flush()

		collection.words.append(word.id)
		collection.translatedWords.append(data[i]['TranslatedText'])
		collection.fromLanguage.append(data[i]['From'])

		user = session.query(User).filter_by(token=token).first()
		collection.creator = user.userId
		collection.creator_token = token

	collection.fromLanguage = list(set(collection.fromLanguage))
	collection.toLanguage = toLanguage

	session.add(collection)
	session.flush()

	return collection




