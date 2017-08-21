"""
----------------------------------------------------------------------
Authors: Nicolai van Niekerk
----------------------------------------------------------------------
Initialises the 'app' object to a flask instance and registers
relevant blueprints.
----------------------------------------------------------------------
"""

from flask import Flask
from verification.controllers import verify
from image_processing.controllers import extract

app = Flask(__name__)

app.register_blueprint(verify)
app.register_blueprint(extract)
