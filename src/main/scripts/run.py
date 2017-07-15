import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from server import app
"""
----------------------------------------------------------------------
Author: Nicolai van Niekerk
----------------------------------------------------------------------
Starts the server
----------------------------------------------------------------------
"""

app.run(debug=False)
