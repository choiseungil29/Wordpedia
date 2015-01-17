import os
import sys
import logging

from Wordpedia import app
from Wordpedia import urls

if __name__ == '__main__':
	app.run(debug=True)