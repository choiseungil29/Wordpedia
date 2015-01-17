from flask import Flask
from flask import render_template, request

from microsofttranslator import Translator

from Wordpedia import app

import json
import urllib

translator = Translator('Wordpedia', 'f1wB2fFCQMVoKPTFqPxMwO79Qxg816xYE7Y5eNF4lBk=')

@app.route('/')
def helloworld():
	return 'Hello World!'

#@app.route('/translate')
#def translate():
#	return translator.translate('hello', 'ko')

@app.route('/translate/<path:toLang>', methods=['GET'])
def translates(toLang):
	resultDic = {}
	for fromText in request.values.getlist('w'):
		resultDic[fromText] = translator.translate(fromText, toLang, translator.detect_language(fromText))
	return json.dumps(resultDic, ensure_ascii=False)

@app.route('/test')
def test():
	return translator.detect_language('hi')


'''Translate Language Code
http://msdn.microsoft.com/en-us/library/hh456380.aspx
'''