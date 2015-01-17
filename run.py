from Wordpedia import app

import Wordpedia.urls

import os
import sys
import logging

app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)