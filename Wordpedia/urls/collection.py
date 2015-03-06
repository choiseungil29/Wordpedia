#-*- coding: utf-8 -*-

from flask import request, Response

from sqlalchemy.orm.exc import NoResultFound

from microsofttranslator import Translator

from wordpedia import app
from wordpedia import session

from wordpedia.model.collection import Collection
from wordpedia.model.word import Word

import json

t = Translator('Wordpedia', 'f1wB2fFCQMVoKPTFqPxMwO79Qxg816xYE7Y5eNF4lBk=')

@app.route('/collection/create', methods=['GET', 'POST'])
def create():
	fromLanguage = request.args.get('from')
	toLanguage = request.args.get('to')
	words = translate(request.values.getlist('w'), fromLanguage, toLanguage)
	return json.dumps(words, ensure_ascii=False)

def translate(words, fromLanguage, toLanguage):
	result = {}
	result['result'] = {}

	data = t.translate_array(words, toLanguage)
	for i in range(0, len(words)):

		word = session.query(Word).filter(Word.id == words[i]).first()
		if word is None:
			word = Word(words[i]) # json데이터 집어넣어야
			word.refCount = json.dumps({ 'refCount': {data[i]['From']: 0} })

			session.add(word)
			session.flush()

		refs = json.loads(str(word.refCount))
		if data[i]['From'] in refs:
			refs[data[i]['From']] += 1
		else:
			refs[data[i]['From']] = 1

		word.refCount = json.dumps(refs)

		result[word.id] = {}
		result[word.id]['translatedText'] = data[i]['TranslatedText']
		result[word.id]['refCount'] = refs

		session.commit()

	return result










