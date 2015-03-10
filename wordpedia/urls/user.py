#-*- coding: utf-8 -*-

from flask import request, Response

from wordpedia import app
from wordpedia import session

from wordpedia.model.user import User

from sqlalchemy.orm.exc import MultipleResultsFound
from sqlalchemy.orm.exc import NoResultFound

import json

@app.route('/login', methods=['GET', 'POST'])
def login():
	id = request.args.get('id')
	password = request.args.get('pw')
	result = {}

	query = session.query(User).filter_by(userId=id)

	try:
		user = query.one()
		if user.pw != password:
			raise Exception
	except NoResultFound, e:
		result['requestCode'] = -1
		result['requestMessage'] = u'존재하지 않는 ID입니다'
		return json.dumps(result, ensure_ascii=False)
	except MultipleResultsFound, e:
		result['requestCode'] = -2
		result['requestMessage'] = u'잘못 만들어진 ID입니다.'
		return json.dumps(result, ensure_ascii=False)
	except:
		result['requestCode'] = -3
		result['requestMessage'] = u'비밀번호가 다릅니다'
		return json.dumps(result, ensure_ascii=False)
	
	result = {}

	user = session.query(User).filter_by(token=user.token).first()
	if user is None:
		return '존재하지 않는 유저입니다'
		
	result['requestCode'] = 1
	result['requestMessage'] = u'로그인에 성공했습니다.'
	result['id'] = user.id
	result['token'] = user.token
	"""result['collections'] = []
	for collection in user.collections.all():
		item = {}
		item['id'] = collection.id
		item['refs'] = collection.refCount
		item['from'] = collection.fromLanguage
		item['to'] = collection.toLanguage
		item['words'] = collection.words
		item['translatedWords'] = collection.translatedWords
		item['createDate'] = collection.createDate.strftime('%Y/%m/%d')
		item['title'] = collection.title
		result['collections'].append(item)"""

	return json.dumps(result, ensure_ascii=False)

@app.route('/logout', methods=['POST', 'GET'])
def logout():
	pass

@app.route('/signup', methods=['GET', 'POST'])
def signup():
	id = request.args['id']
	pw = request.args['pw']

	user = User(id, pw)

	result = {}

	if session.query(User).filter_by(userId=id).count() > 0:
		result['requestCode'] = -1
		result['requestMessage'] = u'이미 존재하는 ID입니다.'
		return json.dumps(result, ensure_ascii=False)

	try:
		session.add(user)
		session.commit()
	except e:
		result['requestCode'] = -1
		result['requestMessage'] = u'잘못된 값입니다.'
		return json.dumps(result, ensure_ascii=False)

	result['requestCode'] = 1
	result['requestMessage'] = u'회원가입에 성공했습니다.'
	result['id'] = user.userId
	result['pw'] = user.pw
	result['token'] = user.token

	return json.dumps(result, ensure_ascii=False)





	
