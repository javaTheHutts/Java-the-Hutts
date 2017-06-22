"""
----------------------------------------------------------------------
Author: Nicolai van Niekerk
----------------------------------------------------------------------
Handles all requests relevant to the validation service of the API
----------------------------------------------------------------------
"""

from flask import Blueprint, jsonify
validate = Blueprint('validate', __name__)

@validate.route('/validate', methods=['POST'])
def validateId():
    """
        ----------------------------------------------------------------------
        Author: Nicolai van Niekerk
        ----------------------------------------------------------------------
        Sample function to return a match percentage of two received faces/images
        ----------------------------------------------------------------------
        URL: http://localhost:5000/validate
        ----------------------------------------------------------------------
        """
    result = {
        "Percentage Match": 97
    }
    return jsonify(result)