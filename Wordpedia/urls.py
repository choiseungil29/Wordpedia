from flask import Flask
from flask import render_template, request

from microsoft import Translator
from apiclient.discovery import build

from Wordpedia import app
from Wordpedia import db

from model.user import User

import json

t = Translator('Wordpedia', 'f1wB2fFCQMVoKPTFqPxMwO79Qxg816xYE7Y5eNF4lBk=')
s = build('translate', 'v2', developerKey='AIzaSyBBvoBtHDYC4iUH-V5gVQ58DnaUTaMwbe4')

db.create_all()

@app.route('/')
def helloworld():
	return 'Hello World!'

@app.route('/translate/<path:company>/<path:to_lang>', methods=['GET', 'POST'])
def test(company, to_lang):
	resultDic = {}
	if company == 'g':
		for item in request.values.getlist('w'):
			resultDic[item] = s.translations().list(q=[item], target=to_lang).execute()

	elif company == 'm':
		for item in request.values.getlist('w'):
			resultDic[item] = t.getTranslations(item, to_lang)

	return json.dumps(resultDic, ensure_ascii=False)

@app.route('/signup', methods=['POST', 'GET'])
def signup():
	id = request.args['id']
	pw = request.args['pw']

	user = User(id, pw)

	if db.session.query(User).filter_by(id=id).count() > 0:
		return 'already User : ' + id

	db.session.add(user)
	db.session.commit()

	return 'Success! ' + user.id + ', ' + user.pw 

@app.route('/login', methods=['POST'])
def login():
	id = request.args.get('id')
	password = request.args.get('pw')

'''Translate Language Code
http://msdn.microsoft.com/en-us/library/hh456380.aspx
'''