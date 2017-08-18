"""
----------------------------------------------------------------------
Author(s): Nicolai van Niekerk, Stephan Nell
----------------------------------------------------------------------
Handles all requests relevant to the extraction service of the API.
----------------------------------------------------------------------
"""
import cv2
import base64
import numpy as np
from image_processing.sample_extract import TextExtractor
from image_processing.sample_extract import FaceExtractor
from imutils.convenience import url_to_image
from flask import Blueprint, jsonify, request, make_response


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
            image = _grab_image(stream=request.files["idPhoto"])
        # Otherwise, assume that a URL was passed in.
        else:
            # Grab the URL from the request.
            url = request.args.get("url", None)
            # If the URL is None, then return an error.
            if url is None:
                data["error"] = "No URL provided."
                return jsonify(data)
                # Load the image and convert.
            image = _grab_image(url=url)

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

        # Extract test from image
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
            image = _grab_image(stream=request.files["idPhoto"])
        # otherwise, assume that a URL was passed in
        else:
            # grab the URL from the request
            url = request.args.get("url", None)
            # if the URL is None, then return an error
            if url is None:
                data["error"] = "No URL provided."
                return jsonify(data)
            # load the image and convert
            image = _grab_image(url=url)
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
            image = _grab_image(stream=request.files["idPhoto"])
        # otherwise, assume that a URL was passed in
        else:
            # grab the URL from the request
            url = request.args.get("url", None)
            # if the URL is None, then return an error
            if url is None:
                data["error"] = "No URL provided."
                return jsonify(data)
            # load the image and convert
            image = _grab_image(url=url)
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

        # Extract test from image
        extractor = TextExtractor(preferences)
        result = extractor.extract(image)

        response = face_extraction_response(image, result)

        return response


def _grab_image(path=None, stream=None, url=None):
    """
    This function grabs the image from URL, or image path and applies necessary changes to the grabbed
    images so that the image is compatible with OpenCV operation.
    Author(s):
        Stephan Nell
    Args:
        path (str): The path to the image if it reside on disk
        stream (str): A stream of text representing where on the internet the image resides
        url(str): Url representing a path to where an image should be fetched.
    Returns:
        (:obj:'OpenCV image'): Image that is now compatible with OpenCV operations
    TODO:
        Return a Json error indicating file not found
    """
    # If the path is not None, then load the image from disk. Example: payload = {"image": open("id.jpg", "rb")}
    if path is not None:
        image = cv2.imread(path)
    # otherwise, the image does not reside on disk
    else:
        # if the URL is not None, then download the image
        if url is not None:
            return url_to_image(url)
        # if the stream is not None, then the image has been uploaded
        elif stream is not None:
            # Example: "http://www.pyimagesearch.com/wp-content/uploads/2015/05/obama.jpg"
            data = stream.read()
            image = np.asarray(bytearray(data), dtype="uint8")
            image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    return image


def face_extraction_response(image, text_extract_result=None):
    """
    This function converts the extracted cv2 image and converts it
    to a jpg image. Furthermore, the jpg image is converted to
    Base64 jpg type and returned. If text extraction results are provided
    the response will contain the data of text extraction result as well.
    Author(s):
        Stephan Nell
    Args:
        image: The cv2 (numpy) image that should be converted to jpg
        text_extract_result (dict) the extracted text results
    Returns:
        (:obj:'Response'): The response object that contains the information for HTTP transmissiond
    """
    extractor = FaceExtractor()
    result = extractor.extract(image)
    _, buffer = cv2.imencode('.jpg', result)
    # replace base64 indicator for the first occurrence
    jpg_img = str(base64.b64encode(buffer)).replace("b", ",", 1)
    # apply base64 jpg encoding
    jpg_img = 'data:image/jpg;base64' + jpg_img
    # cleanup interference
    jpg_img = jpg_img.replace("'", "")
    data = jsonify(
        {
            "extracted_face": jpg_img,
            "text_extract_result": text_extract_result
        })
    # prepare response
    response = make_response(data)
    response.mimetype = 'multipart/form-data'
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'

    return response
