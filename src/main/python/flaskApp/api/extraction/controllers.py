"""
----------------------------------------------------------------------
Author: Nicolai van Niekerk
----------------------------------------------------------------------
Handles all requests relevant to the extraction service of the API
----------------------------------------------------------------------
"""

from flask import Blueprint, jsonify, request

extract = Blueprint('extract', __name__)


@extract.route('/extractText', methods=['POST'])
def extractText():
    """
    ----------------------------------------------------------------------
    Author: Nicolai van Niekerk
    ----------------------------------------------------------------------
    Sample function to extract text from image received
    ----------------------------------------------------------------------
    URL: http://localhost:5000/extractText
    ----------------------------------------------------------------------
    """
    image = request.files.get("image")
    text = {
        "Surname": "Doe",
        "Names": "John Jane",
        "Sex": "M",
        "Nationality": "RSA",
        "Identity Number": "6944585228083",
        "Date of Birth": "06-05-1996",
        "Country of Birth": "RSA",
        "Status": "Citizen"
    }
    return jsonify({"Extracted Fields": text})


@extract.route('/extractFace', methods=['POST'])
def extractFace():
    """
    ----------------------------------------------------------------------
    Author: Nicolai van Niekerk
    ----------------------------------------------------------------------
    Sample function to extract face from image received
    ----------------------------------------------------------------------
    URL: http://localhost:5000/extractFace
    ----------------------------------------------------------------------
    """
    image = request.files.get("image")
    face = "jklanskjcbniugciuhncoiaksc6565"
    return jsonify({"Extracted Face": face})


@extract.route('/extractAll', methods=['POST'])
def extractAll():
    """
    ----------------------------------------------------------------------
    Author: Nicolai van Niekerk
    ----------------------------------------------------------------------
    Sample function to extract face and text from image received
    ----------------------------------------------------------------------
    URL: http://localhost:5000/extractAll
    ----------------------------------------------------------------------
    """
    image = request.files.get("image")
    print(image)
    data = {
        "Surname": "Doe",
        "Names": "John Jane",
        "Sex": "M",
        "Nationality": "RSA",
        "Identity Number": "6944585228083",
        "Date of Birth": "06-05-1996",
        "Country of Birth": "RSA",
        "Status": "Citizen",
        "Face": "jklanskjcbniugciuhncoiaksc6565"
    }
    return jsonify({"Extracted data": data})
