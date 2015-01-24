#wrapping api for microsoft translator api

try:
	import simplejson as json
except ImportError:
	import json

import requests
import six
import warnings
import logging

from microsofttranslator import Translator

class ArgumentOutOfRangeException(Exception):
	def __init__(self, message):
		self.message = message.replace('ArgumentOutOfRangeException : ', '')
		super(ArgumentOutOfException, self).__init__(self.message)

class TranslateApiException(Exception):
	def __init__(self, message, *args):
		self.message = message.replace('TranslateApiException : ', '')
		super(TranslateApiException, self).__init__(self.message, *args)

class Translator(Translator):
	def __init__(self, client_id, client_secret, debug=False):
		super(Translator, self).__init__(client_id, client_secret, debug=debug)

	def getTranslations(self, text, to_lang, from_lang=None, maxTranslations=10):
		params = {
			'text': text,
			'to': to_lang,
			'maxTranslations': maxTranslations
		}
		if from_lang is not None:
			params['from'] = from_lang

		return self.call('GetTranslations', params)

if __name__ == '__main__':
	t = Translator('Wordpedia', 'f1wB2fFCQMVoKPTFqPxMwO79Qxg816xYE7Y5eNF4lBk=')
	print t.getTranslations('hi', 'ko')








