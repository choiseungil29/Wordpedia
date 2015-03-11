#-*- coding: utf-8 -*-

from flask import request, Response

from sqlalchemy.orm.exc import NoResultFound

from microsofttranslator import Translator

from wordpedia import app
from wordpedia import session

from wordpedia.model.collection import Collection
from wordpedia.model.word import Word
from wordpedia.model.user import User
from wordpedia.model.comment import Comment

import json

@app.route('/comment/add', methods=['POST', 'GET'])
def add():
	targetWord = request.args['word']
	targetCollectionId = request.args['collectionId']
	content = request.args['comment']

	result = {}

	try:
		session.query(Word).filter_by(id=targetWord).one()
		session.query(Collection).filter_by(id=targetCollectionId).one()
	except:
		result['requestCode'] = -1
		result['requestMessage'] = u'코멘트 작성을 실패했습니다. ' + targetWord
		return json.dumps(result, ensure_ascii=False);

	try:
		user = session.query(User).filter_by(userId=request.args['id']).filter_by(token=request.headers['token']).one()
	except:
		result['requestCode'] = -1
		result['requestMessage'] = u'코멘트 작성을 실패했습니다..'
		return json.dumps(result, ensure_ascii=False);

	comment = Comment()
	comment.contents = content
	comment.collection_id = targetCollectionId
	comment.word_id = targetWord
	comment.creator = user.userId
	comment.creator_token = user.token

	result['requestCode'] = 1
	result['requestMessage'] = u'코멘트 작성을 성공했습니다.'

	session.add(comment)
	session.commit()

	return json.dumps(result, ensure_ascii=False)



