"""
----------------------------------------------------------------------
Author(s): Nicolai van Niekerk, Stephan Nell
----------------------------------------------------------------------
Handles all requests relevant to the extraction service of the API.
----------------------------------------------------------------------
"""
from image_processing.sample_extract import TextExtractor
from flask import Blueprint, jsonify, request
from hutts_utils.image_handling import grab_image, face_extraction_response

extract = Blueprint('extract', __name__)


@extract.route('/extractText', methods=['POST'])
def extract_text():
    """
    ----------------------------------------------------------------------
    Author(s): Nicolai van Niekerk, Stephan Nell
    ----------------------------------------------------------------------
    Sample function to extract text from image received.
    ----------------------------------------------------------------------
    URL: http://localhost:5000/extractText
    ----------------------------------------------------------------------
    """
    # Initialize the data dictionary to be returned by the request.
    data = {"success": False}

    # Check to see if this is a post request.
    if request.method == "POST":
        # Check to see if an image was uploaded.
        if request.files.get("idPhoto", None) is not None:
            # Grab the uploaded image.
            image = grab_image(stream=request.files["idPhoto"])
        # Otherwise, assume that a URL was passed in.
        else:
            # Grab the URL from the request.
            url = request.args.get("url", None)
            # If the URL is None, then return an error.
            if url is None:
                data["error"] = "No URL provided."
                return jsonify(data)
                # Load the image and convert.
            image = grab_image(url=url)

        # Grab additional parameters specifying techniques
        preferences = {}

        if 'blur_technique' in request.form:
            preferences['blur_method'] = request.form['blur_technique']
        if 'threshold_technique' in request.form:
            preferences['threshold_method'] = request.form['threshold_technique']
        if 'remove_face' in request.form:
            preferences['remove_face'] = request.form['remove_face']
        if 'remove_barcode' in request.form:
            preferences['remove_barcode'] = request.form['remove_barcode']
        if 'color' in request.form:
            preferences['color'] = request.form['color']
        if 'id_type' in request.form:
            preferences['id_type'] = request.form['id_type']

        # Extract text from image
        extractor = TextExtractor(preferences)
        result = extractor.extract(image)
    return jsonify(result)


@extract.route('/extractFace', methods=['POST'])
def extract_face():
    """
    ----------------------------------------------------------------------
    Author(s): Nicolai van Niekerk, Stephan Nell
    ----------------------------------------------------------------------
    Sample function to extract face from image received
    ----------------------------------------------------------------------
    URL: http://localhost:5000/extractFace
    ----------------------------------------------------------------------
    """
    # initialize the data dictionary to be returned by the request
    data = {"success": False}

    # check to see if this is a post request
    if request.method == "POST":
        # check to see if an image was uploaded
        if request.files.get("idPhoto", None) is not None:
            # grab the uploaded image
            image = grab_image(stream=request.files["idPhoto"])
        # otherwise, assume that a URL was passed in
        else:
            # grab the URL from the request
            url = request.args.get("url", None)
            # if the URL is None, then return an error
            if url is None:
                data["error"] = "No URL provided."
                return jsonify(data)
            # load the image and convert
            image = grab_image(url=url)
    # Call open CV commands here with the extracted image
    response = face_extraction_response(image)
    return response


@extract.route('/extractAll', methods=['POST'])
def extract_all():
    """
    ----------------------------------------------------------------------
    Author(s): Nicolai van Niekerk, Stephan Nell
    ----------------------------------------------------------------------
    Sample function to extract face and text from image received
    ----------------------------------------------------------------------
    URL: http://localhost:5000/extractAll
    ----------------------------------------------------------------------
    """
    # initialize the data dictionary to be returned by the request
    data = {"success": False}
    # check to see if this is a post request
    if request.method == "POST":
        # check to see if an image was uploaded
        if request.files.get("idPhoto", None) is not None:
            # grab the uploaded image
            image = grab_image(stream=request.files["idPhoto"])
        # otherwise, assume that a URL was passed in
        else:
            # grab the URL from the request
            url = request.args.get("url", None)
            # if the URL is None, then return an error
            if url is None:
                data["error"] = "No URL provided."
                return jsonify(data)
            # load the image and convert
            image = grab_image(url=url)
        # Call open CV commands here with the extracted image
        # Grab additional parameters specifying techniques
        preferences = {}

        if 'blur_technique' in request.form:
            preferences['blur_method'] = request.form['blur_technique']
        if 'threshold_technique' in request.form:
            preferences['threshold_method'] = request.form['threshold_technique']
        if 'remove_face' in request.form:
            preferences['remove_face'] = request.form['remove_face']
        if 'remove_barcode' in request.form:
            preferences['remove_barcode'] = request.form['remove_barcode']
        if 'color' in request.form:
            preferences['color'] = request.form['color']
        if 'id_type' in request.form:
            preferences['id_type'] = request.form['id_type']

        # Extract test from image
        extractor = TextExtractor(preferences)
        result = extractor.extract(image)

        response = face_extraction_response(image, result)

        return response
