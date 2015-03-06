#-*- coding: utf-8 -*-

from flask import request

from sqlalchemy.orm.exc import NoResultFound

from wordpedia import app
from wordpedia import session

from wordpedia.model.word import Word

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