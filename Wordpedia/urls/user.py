#-*- coding: utf-8 -*-

from flask import request, Response

from wordpedia import app
from wordpedia import db

from wordpedia.model.user import User

from sqlalchemy.orm.exc import MultipleResultsFound
from sqlalchemy.orm.exc import NoResultFound

import json

@app.route('/login', methods=['GET', 'POST'])
def login():
	id = request.args.get('id')
	password = request.args.get('pw')
	result = {}

	query = db.session.query(User).filter(User.id == id)

	try:
		user = query.one()
	except NoResultFound, e:
		result['requestCode'] = -1
		result['requestMessage'] = u'존재하지 않는 ID입니다'
		return json.dumps(result, ensure_ascii=False)
	except MultipleResultsFound, e:
		result['requestCode'] = -2
		result['requestMessage'] = u'잘못 만들어진 ID입니다.'
		return json.dumps(result, ensure_ascii=False)

	result['requestCode'] = 1
	result['resultMessage'] = u'로그인에 성공했습니다.'
	result['id'] = user.id
	result['token'] = user.token

	return json.dumps(result, ensure_ascii=False)

@app.route('/logout', methods=['POST'])
def logout():
	pass

@app.route('/signup', methods=['POST', 'GET'])
def signup():
	id = request.args['id']
	pw = request.args['pw']

	user = User(id, pw)

	result = {}

	if db.session.query(User).filter(User.id == id).count() > 0:
		result['requestCode'] = -1
		result['requestMessage'] = u'이미 존재하는 ID입니다.'
		return json.dumps(result, ensure_ascii=False)

	try:
		db.session.add(user)
		db.session.commit()
	except e:
		result['requestCode'] = -1
		result['requestMessage'] = u'잘못된 값입니다.'
		return json.dumps(result, ensure_ascii=False)

	result['requestCode'] = 1
	result['requestMessage'] = u'회원가입에 성공했습니다.'
	result['id'] = user.id
	result['pw'] = user.pw
	result['token'] = user.token

	return json.dumps(result, ensure_ascii=False)