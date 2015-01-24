#-*- coding: utf-8 -*-

import sys

from apiclient.discovery import build

service = build('translate', 'v2', developerKey='AIzaSyBBvoBtHDYC4iUH-V5gVQ58DnaUTaMwbe4')

def translations():
	print service.translations().list(
		source='ko',
		target='en',
		q=['안녕'.decode('utf-8'), 'car'.decode('utf-8')]
		).execute()

def detections(list):
	print service.detections().list(
		q=list).execute()

def languages():
	print service.languages().list(
		target='en').execute()

if __name__ == '__main__':
	translations()
	#detections(['hi', '안녕하세요'.decode('utf-8')])