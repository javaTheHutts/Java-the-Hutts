import os
import sys

from flask import Flask
from validation.controllers import validate
from extraction.controllers import extract

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
