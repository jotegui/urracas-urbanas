__author__ = '@jotegui'

import logging
import sqlite3
from flask import Flask, session
from flask.ext.mail import Mail

# Main app
app = Flask(__name__)
app.config.from_object("config")
print app.config['DATABASE']

from logging import FileHandler
log_path = 'C:\\AppServ\\www\\urracas\\log.txt'
file_handler = FileHandler(log_path)
file_handler.setLevel(logging.WARNING)
app.logger.addHandler(file_handler)

# Mail app
mail = Mail(app)

import views
import views_admin
import views_api