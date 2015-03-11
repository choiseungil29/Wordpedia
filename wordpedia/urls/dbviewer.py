#-*- coding: utf-8 -*-

from flask import request

from sqlalchemy.orm.exc import NoResultFound

from wordpedia import app
from wordpedia import session

from wordpedia.model.word import Word
from wordpedia.model.user import User
from wordpedia.model.comment import Comment
from wordpedia.model.collection import Collection

import json


def setCollection(collection):
	result = {}
	result['id'] = collection.id
	result['refs'] = collection.refCount
	result['from'] = collection.fromLanguage
	result['to'] = collection.toLanguage
	result['words'] = collection.words
	result['translatedWords'] = collection.translatedWords
	result['createDate'] = collection.createDate.strftime('%Y/%m/%d')
	result['title'] = collection.title
	result['creatorToken'] = collection.creator_token
	result['creator'] = collection.creator
	result['comments'] = []
	for comment in collection.comments.all():
		item = {}
		item['comment'] = comment.contents
		item['creator'] = comment.creator
		item['createDate'] = comment.createDate.strftime('%Y/%m/%d')
		result['comments'].append(item)
	return result


























