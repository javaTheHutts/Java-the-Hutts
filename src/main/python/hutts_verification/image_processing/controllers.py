"""
Handles all requests relevant to the extraction service of the API.
"""
import base64
import cv2
from hutts_verification.image_processing.sample_extract import TextExtractor
from flask import Blueprint, jsonify, request, make_response
from hutts_verification.utils.image_handling import grab_image
from hutts_verification.image_processing.sample_extract import FaceExtractor
from hutts_verification.utils.hutts_logger import logger

__authors__ = "Nicolai van Niekerk, Stephan Nell"
__copyright__ = "Copyright 2017, Java the Hutts"
__license__ = "BSD"
__maintainer__ = "Nicolai van Niekerk"
__email__ = "nicvaniek@gmail.com"
__status__ = "Development"


extract = Blueprint('extract', __name__)


@extract.route('/extractText', methods=['POST'])
def extract_text():
    """
    Sample function to extract text from image received.

    URL: http://localhost:5000/extractText.

    """
    # Initialize the data dictionary to be returned by the request.
    data = {"success": False}

    # Check to see if this is a post request.
    if request.method == "POST":
        # Check to see if an image was uploaded.
        if request.get_json().get("idPhoto", None) is not None:
            # Grab the uploaded image.
            image = grab_image(string=request.get_json()["idPhoto"])
        # Otherwise, assume that a URL was passed in.
        else:
            # Grab the URL from the request.
            url = request.get_json().get("url", None)
            # If the URL is None, then return an error.
            if url is None:
                data["error"] = "No URL provided."
                return jsonify(data)
                # Load the image and convert.
            image = grab_image(url=url)

        # Grab additional parameters specifying techniques
        preferences = {}

        if 'blur_technique' in request.get_json():
            preferences['blur_method'] = request.get_json()['blur_technique']
        if 'threshold_technique' in request.get_json():
            preferences['threshold_method'] = request.get_json()['threshold_technique']
        if 'remove_face' in request.get_json():
            preferences['remove_face'] = request.get_json()['remove_face']
        if 'remove_barcode' in request.get_json():
            preferences['remove_barcode'] = request.get_json()['remove_barcode']
        if 'color' in request.get_json():
            preferences['color'] = request.get_json()['color']
        if 'id_type' in request.get_json():
            preferences['id_type'] = request.get_json()['id_type']
        if 'useIO' in request.get_json():
            preferences['useIO'] = request.get_json()['useIO'] == 'true'
        else:
            preferences['useIO'] = False

        # Extract text from image
        extractor = TextExtractor(preferences)
        result = extractor.extract(image)
    return jsonify(result)


@extract.route('/extractFace', methods=['POST'])
def extract_face():
    """
    Sample function to extract face from image received.

    URL: http://localhost:5000/extractFace.

    """
    # initialize the data dictionary to be returned by the request
    data = {"success": False}

    # check to see if this is a post request
    if request.method == "POST":
        # check to see if an image was uploaded
        if request.get_json().get("idPhoto", None) is not None:
            # grab the uploaded image
            image = grab_image(string=request.get_json()["idPhoto"])
        # otherwise, assume that a URL was passed in
        else:
            # grab the URL from the request
            url = request.get_json().get("url", None)
            # if the URL is None, then return an error
            if url is None:
                data["error"] = "No URL provided."
                return jsonify(data)
            # load the image and convert
            image = grab_image(url=url)

    # Add preferences
    preferences = {}
    if 'useIO' in request.get_json():
        preferences['useIO'] = request.get_json()['useIO'] == 'true'
    # Call open CV commands here with the extracted image
    response = face_extraction_response(preferences['useIO'], image)
    return response


@extract.route('/extractAll', methods=['POST'])
def extract_all():
    """
    Sample function to extract face and text from image received.

    URL: http://localhost:5000/extractAll.

    """
    # initialize the data dictionary to be returned by the request
    data = {"success": False}
    # check to see if this is a post request
    if request.method == "POST":
        # check to see if an image was uploaded
        if request.get_json().get("idPhoto", None) is not None:
            # grab the uploaded image
            image = grab_image(string=request.get_json()["idPhoto"])
        # otherwise, assume that a URL was passed in
        else:
            # grab the URL from the request
            url = request.get_json().get("url", None)
            # if the URL is None, then return an error
            if url is None:
                data["error"] = "No URL provided."
                return jsonify(data)
            # load the image and convert
            image = grab_image(url=url)
        # Call open CV commands here with the extracted image
        # Grab additional parameters specifying techniques
        preferences = {}

        if 'blur_technique' in request.get_json():
            preferences['blur_method'] = request.get_json()['blur_technique']
        if 'threshold_technique' in request.get_json():
            preferences['threshold_method'] = request.get_json()['threshold_technique']
        if 'remove_face' in request.get_json():
            preferences['remove_face'] = request.get_json()['remove_face']
        if 'remove_barcode' in request.get_json():
            preferences['remove_barcode'] = request.get_json()['remove_barcode']
        if 'color' in request.get_json():
            preferences['color'] = request.get_json()['color']
        if 'id_type' in request.get_json():
            preferences['id_type'] = request.get_json()['id_type']
        if 'useIO' in request.get_json():
            preferences['useIO'] = request.get_json()['useIO'] == 'true'
        else:
            preferences['useIO'] = False

        # Extract test from image
        extractor = TextExtractor(preferences)
        result = extractor.extract(image)

        response = face_extraction_response(preferences['useIO'], image, result)

        return response


def face_extraction_response(use_io, image, text_extract_result=None):
    """
    This function converts the extracted cv2 image and converts it
    to a jpg image. Furthermore, the jpg image is converted to
    Base64 jpg type and returned. If text extraction results are provided
    the response will contain the data of text extraction result as well.

    :param use_io (boolean): Whether or not images should be written to disk.
    :param image (obj): The cv2 (numpy) image that should be converted to jpg.
    :param text_extract_result (dict): The extracted text results.

    Returns:
        - (obj): The response object that contains the information for HTTP transmission.

    """
    extractor = FaceExtractor()
    result = extractor.extract(image, use_io)
    _, buffer = cv2.imencode('.jpg', result)
    # replace base64 indicator for the first occurrence and apply apply base64 jpg encoding
    logger.info("Converting to Base64")
    jpg_img = ('data:image/jpg;base64' + str(base64.b64encode(buffer)).replace("b", ",", 1)).replace("'", "")
    temp_dict = {"extracted_face": jpg_img}
    if text_extract_result:
        temp_dict["text_extract_result"] = text_extract_result
    data = jsonify(temp_dict)
    # prepare response
    logger.info("Preparing Response")
    response = make_response(data)
    response.mimetype = 'multipart/form-data'
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'

    return response
