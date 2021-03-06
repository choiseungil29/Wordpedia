#-*- coding: utf-8 -*-

from flask import request, Response

from wordpedia import app
from wordpedia import db

from wordpedia.microsoft import Translator
from apiclient.discovery import build

from wordpedia.model.word import Word

import json

t = Translator('Wordpedia', 'f1wB2fFCQMVoKPTFqPxMwO79Qxg816xYE7Y5eNF4lBk=')
s = build('translate', 'v2', developerKey='AIzaSyBBvoBtHDYC4iUH-V5gVQ58DnaUTaMwbe4')

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

@app.route('/translate/v2/<path:to_lang>', methods=['POST'])
def translate(to_lang):
	wordMap = {}

	for queryItem in request.values.getlist('w'):
		if queryItem in wordMap:
			continue
		data = s.translations().list(q=[queryItem], target=to_lang).execute()['translations']
		for jsonItem in data:
			wordMap[queryItem] = Word(queryItem, jsonItem['translatedText'], jsonItem['detectedSourceLanguage'])

	result = {}
	for item in wordMap.keys():
		result[item] = wordMap[item].translatedWord
	return json.dumps(result, ensure_ascii=False)

'''uses google translate API'''

'''Translate Language Code
http://msdn.microsoft.com/en-us/library/hh456380.aspx
'''