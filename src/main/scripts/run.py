"""
----------------------------------------------------------------------
Author: Nicolai van Niekerk
----------------------------------------------------------------------
Starts the server
----------------------------------------------------------------------
"""

import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '../../'))
sys.path.append(os.path.abspath('./' + '../../'))

from main.python.flaskApp.api import app

app.run(debug=False)
