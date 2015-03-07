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
	
	try:
		token = request.headers.get('token')
		collection = createCollection(request.values.getlist('w'), request.args['to'])
		addCollectionToUser(token, collection)
	except ValueError, e:
		return 'error. failed create collection'
	except:
		return token

	session.commit()
	return json.dumps(collection.words, ensure_ascii=False)

@app.route('/collection/copy')
def copy():
	"""
	다른 유저에게 collection id값을 복사해준다.
	"""

	try:
		token = request.headers.get('token')
		User.tokenCheck(token)
	except:
		return 'error.'

	collectionId = request.args['colId']
	userToken = request.args['token']

	user = session.query(User).filter_by(token=token).first()
	if user is None:
		raise ValueError


def createCollection(words, toLanguage):
	result = {}
	collection = Collection()

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

	collection.fromLanguage = list(set(collection.fromLanguage))
	collection.toLanguage = toLanguage

	session.add(collection)
	session.flush()

	return collection

def addCollectionToUser(token, collection):
	user = session.query(User).filter_by(token=token).first()

	user.collections.append(collection)
	session.flush()

	return user







