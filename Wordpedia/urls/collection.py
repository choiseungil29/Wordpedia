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
	'''
	params:
	requst
	 w : word list.
	 to : language code that want to return
	header
	 token : user token
	'''
	try:
		collection = createCollection(request.values.getlist('w'), request.args.get('to'))
	except e:
		return 'error. failed create collection'

	addCollectionToUser(request.header.get('token'), collection)

	return json.dumps(collection.words, ensure_ascii=False)
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
		session.commit()

		collection.words.append(word.id)
		collection.translatedWords.append(data[i]['TranslatedText'])
		collection.fromLanguage.append(data[i]['From'])

	collection.fromLanguage = list(set(collection.fromLanguage))
	collection.toLanguage = toLanguage

	session.add(collection)
	session.commit()

	return collection

def addCollectionToUser(token, collection):
	user = session.query(User).filter(token=token)
	user.collections.append(collection)








