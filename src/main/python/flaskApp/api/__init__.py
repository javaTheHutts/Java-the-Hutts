"""
----------------------------------------------------------------------
Author: Nicolai van Niekerk
----------------------------------------------------------------------
Initialises the 'app' object to a flask instance and registers relevant
blueprints
----------------------------------------------------------------------
"""

import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '../..'))

from flask import Flask

app = Flask(__name__)

#Register blueprints
from main.python.flaskApp.api.validation.controllers import validate
from main.python.flaskApp.api.extraction.controllers import extract
app.register_blueprint(validate)
app.register_blueprint(extract)