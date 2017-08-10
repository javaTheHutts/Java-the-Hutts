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
def verify_id():
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
    # image_of_id = request.files.get("id_img")
    # names = request.form['names']
    # surname = request.form['surname']
    # id_number = request.form['id_number']
    # nationality = request.form['nationality']
    # country_of_birth = request.form['cob']
    # status = request.form['status']
    # gender = request.form['gender']
    # date_of_birth = request.form['dob']
    # face = request.files.get('face_img')
    print(request)

    # do stuff to get result

    result = {
        "percent_match": 63
    }
    return jsonify(result)


@validate.route('/verifyFaces', methods=['POST'])
def verify_faces():
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
    # image_of_id = request.files.get("id_img")
    # face = request.files.get("face")

    # do stuff to get result

    result = {
        "percent_match": 63
    }
    return jsonify(result)


@validate.route('/verifyInfo', methods=['POST'])
def verify_info():
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
    # image_of_id = request.files.get("id_img")
    # names = request.form['names']
    # surname = request.form['surname']
    # id_number = request.form['id_number']
    # nationality = request.form['nationality']
    # country_of_birth = request.form['cob']
    # status = request.form['status']
    # gender = request.form['gender']
    # date_of_birth = request.form['dob']

    # do stuff to get result

    result = {
        "percent_match": 63
    }
    return jsonify(result)
