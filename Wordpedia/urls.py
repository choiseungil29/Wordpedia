from flask import Flask
from flask import render_template, request

from microsoft import Translator
from apiclient.discovery import build

from Wordpedia import app

import json

t = Translator('Wordpedia', 'f1wB2fFCQMVoKPTFqPxMwO79Qxg816xYE7Y5eNF4lBk=')
s = build('translate', 'v2', developerKey='AIzaSyBBvoBtHDYC4iUH-V5gVQ58DnaUTaMwbe4')

@app.route('/')
def helloworld():
	return 'Hello World!'

@app.route('/translate/<path:company>/<path:to_lang>', methods=['GET'])
def test(company, to_lang):
	resultDic = {}
	if company == 'g':
		for item in request.values.getlist('w'):
			resultDic[item] = s.translations().list(q=[item], target=to_lang).execute()

	elif company == 'm':
		for item in request.values.getlist('w'):
			resultDic[item] = t.getTranslations(item, to_lang)

	return json.dumps(resultDic, ensure_ascii=False)

'''Translate Language Code
http://msdn.microsoft.com/en-us/library/hh456380.aspx
'''