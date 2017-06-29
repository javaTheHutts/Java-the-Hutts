"""
----------------------------------------------------------------------
Author: Nicolai van Niekerk
----------------------------------------------------------------------
Handles all requests relevant to the validation service of the API
----------------------------------------------------------------------
"""

from flask import Blueprint, jsonify, request
validate = Blueprint('validate', __name__)


@validate.route('/validateID', methods=['POST'])
def validateId():
    """
        ----------------------------------------------------------------------
        Author: Nicolai van Niekerk
        ----------------------------------------------------------------------
        Sample function to return a match percentage of an ID image and
        provided personal information and picture of face
        ----------------------------------------------------------------------
        URL: http://localhost:5000/validate
        ----------------------------------------------------------------------
        """
    image_of_id = request.files.get("ID")
    name = request.form['name']
    surname = request.form['surname']
    face = request.files.get('face')
    result = {
        "Percentage Match": 63
    }
    return jsonify(result)
