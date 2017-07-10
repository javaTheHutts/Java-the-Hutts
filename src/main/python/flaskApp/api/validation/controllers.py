"""
----------------------------------------------------------------------
Author: Nicolai van Niekerk
----------------------------------------------------------------------
Handles all requests relevant to the validation service of the API
----------------------------------------------------------------------
"""

from flask import Blueprint, jsonify, request
validate = Blueprint('validate', __name__)


@validate.route('/verifyID', methods=['POST'])
def verifyID():
    """
        ----------------------------------------------------------------------
        Author: Nicolai van Niekerk
        ----------------------------------------------------------------------
        Sample function to return a match percentage of an ID image and
        provided personal information and picture of face
        ----------------------------------------------------------------------
        URL: http://localhost:5000/verifyID
        ----------------------------------------------------------------------
        """
    image_of_id = request.files.get("idPhoto")
    names = request.form['names']
    surname = request.form['surname']
    id_number = request.form['idNumber']
    nationality = request.form['Nationality']
    country_of_birth = request.form['cob']
    status = request.form['status']
    gender = request.form['gender']
    date_of_birth = request.form['dob']
    face = request.files.get('userImage')

    # do stuff to get result

    result = {
        "Percentage Match": 63
    }
    return jsonify(result)

@validate.route('/verifyFaces', methods=['POST'])
def verifyFaces():
    """
        ----------------------------------------------------------------------
        Author: Nicolai van Niekerk
        ----------------------------------------------------------------------
        Sample function to return a match percentage of an ID face image and
        picture of face
        ----------------------------------------------------------------------
        URL: http://localhost:5000/verifyFaces
        ----------------------------------------------------------------------
        """
    image_of_id = request.files.get("ID")
    face = request.files.get('face')

    # do stuff to get result

    result = {
        "Percentage Match": 63
    }
    return jsonify(result)

@validate.route('/verifyInfo', methods=['POST'])
def verifyInfo():
    """
        ----------------------------------------------------------------------
        Author: Nicolai van Niekerk
        ----------------------------------------------------------------------
        Sample function to return a match percentage of an ID image and
        provided personal information
        ----------------------------------------------------------------------
        URL: http://localhost:5000/verifyInfo
        ----------------------------------------------------------------------
        """
    image_of_id = request.files.get("idPhoto")
    names = request.form['names']
    surname = request.form['surname']
    id_number = request.form['idNumber']
    nationality = request.form['Nationality']
    country_of_birth = request.form['cob']
    status = request.form['status']
    gender = request.form['gender']
    date_of_birth = request.form['dob']

    # do stuff to get result

    result = {
        "Percentage Match": 63
    }
    return jsonify(result)