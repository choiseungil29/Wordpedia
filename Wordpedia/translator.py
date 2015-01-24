from microsoft import Translator
from apiclient.discovery import build

t = Translator('Wordpedia', 'f1wB2fFCQMVoKPTFqPxMwO79Qxg816xYE7Y5eNF4lBk=')
s = build('translate', 'v2', developerKey='AIzaSyBBvoBtHDYC4iUH-V5gVQ58DnaUTaMwbe4')

def translation(to_lang, list_word):
	for item in list_word:
		m_word = t.getTranslations(item, to_lang)
		g_word = s.translations().list(q=[item], target=to_lang).execute()
		print 'microsoft : ' + str(m_word) + '\n'
		print 'google : ' + str(g_word) + '\n'

if __name__ == '__main__':
	translation('en', ['hi', 'hello', 'fuck'])
