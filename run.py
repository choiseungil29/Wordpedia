import os
import sys
import logging

from wordpedia import app
from wordpedia import urls

if __name__ == '__main__':
	app.run(debug=True)