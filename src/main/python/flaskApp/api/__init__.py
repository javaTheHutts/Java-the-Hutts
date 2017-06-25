from flask import Flask
from main.python.flaskApp.api.validation.controllers import validate
from main.python.flaskApp.api.extraction.controllers import extract
import os
import sys

"""
----------------------------------------------------------------------
Author: Nicolai van Niekerk
----------------------------------------------------------------------
Initialises the 'app' object to a flask instance and registers relevant
blueprints
----------------------------------------------------------------------
"""
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '../..'))

app = Flask(__name__)

app.register_blueprint(validate)
app.register_blueprint(extract)
