#-*- coding: utf-8 -*-

from flask import Flask, request, Response

from microsoft import Translator
from apiclient.discovery import build

from wordpedia import app
from wordpedia import db

from model.word import Word
from model.user import User

from pprint import pprint
from StringIO import StringIO


import json

t = Translator('Wordpedia', 'f1wB2fFCQMVoKPTFqPxMwO79Qxg816xYE7Y5eNF4lBk=')
s = build('translate', 'v2', developerKey='AIzaSyBBvoBtHDYC4iUH-V5gVQ58DnaUTaMwbe4')

db.create_all()

@app.route('/')
def helloworld():
	return 'Hello World!'

@app.route('/translate/<path:company>/<path:to_lang>', methods=['GET', 'POST'])
def translateToCompanies(company, to_lang):
	resultDic = {}
	if company == 'g':
		for item in request.values.getlist('w'):
			resultDic[item] = s.translations().list(q=[item], target=to_lang).execute()

	elif company == 'm':
		for item in request.values.getlist('w'):
			resultDic[item] = t.getTranslations(item, to_lang)

	return json.dumps(resultDic, ensure_ascii=False)

@app.route('/translate/v2/<path:to_lang>', methods=['GET', 'POST'])
def translate(to_lang):
	wordMap = {}

	for queryItem in request.values.getlist('w'):
		if queryItem in wordMap:
			continue
		data = s.translations().list(q=[queryItem], target=to_lang).execute()['translations']
		for jsonItem in data:
			# 여기에 단어 여러개 나왔을때 비교
			wordMap[queryItem] = Word(queryItem, jsonItem['translatedText'], jsonItem['detectedSourceLanguage'])

	result = {}
	for item in wordMap.keys():
		result[item] = wordMap[item].translatedWord
	return json.dumps(result, ensure_ascii=False)

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

'''uses google translate API'''

'''Translate Language Code
http://msdn.microsoft.com/en-us/library/hh456380.aspx
'''