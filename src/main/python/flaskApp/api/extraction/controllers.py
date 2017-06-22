"""
----------------------------------------------------------------------
Author: Nicolai van Niekerk
----------------------------------------------------------------------
Handles all requests relevant to the extraction service of the API
----------------------------------------------------------------------
"""

from flask import Blueprint, jsonify
extract = Blueprint('extract', __name__)

@extract.route('/extract', methods=['POST'])
def extractText():
    """
    ----------------------------------------------------------------------
    Author: Nicolai van Niekerk
    ----------------------------------------------------------------------
    Sample function to extract text from image received
    ----------------------------------------------------------------------
    URL: http://localhost:5000/extract
    ----------------------------------------------------------------------
    """
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