"""
Handles all requests relevant to the verification service of the API.
"""

from hutts_verification.image_processing.sample_extract import TextExtractor
from hutts_verification.image_preprocessing.face_manager import FaceDetector
from hutts_verification.verification.text_verify import TextVerify
from hutts_verification.verification.face_verify import FaceVerify
from flask import jsonify, request, Blueprint
from hutts_verification.utils.hutts_logger import logger
from hutts_verification.utils.image_handling import grab_image
from hutts_verification.utils.pypath import correct_path
from pathlib import Path
import os

__authors__ = "Nicolai van Niekerk, Stephan Nell, Marno Hermann, Andreas Nel"
__copyright__ = "Copyright 2017, Java the Hutts"
__license__ = "BSD"
__maintainer__ = "Nicolai van Niekerk"
__email__ = "nicvaniek@gmail.com"
__status__ = "Development"


verify = Blueprint('verify', __name__)

# Constants path to trained data for Shape Predictor.
CURRENT_LOCATION = os.path.abspath(os.path.dirname(__file__))
SHAPE_PREDICTOR_PATH = correct_path(Path(
                                            Path(CURRENT_LOCATION),
                                            Path(CURRENT_LOCATION).parent,
                                            'image_preprocessing',
                                            'trained_data',
                                            'shape_predictor_face_landmarks.dat'
                                        )
                                    )
FACE_RECOGNITION_PATH = correct_path(Path(
                                            Path(CURRENT_LOCATION),
                                            Path(CURRENT_LOCATION).parent,
                                            'image_preprocessing',
                                            'trained_data',
                                            'dlib_face_recognition_resnet_model_v1.dat'
                                         ))


@verify.route('/verifyID', methods=['POST'])
def verify_id():
    """
    Sample function to return a match percentage of an ID image and
    provided personal information and picture of face.

    URL: http://localhost:5000/verifyID.

    """
    image_of_id, face = receive_faces(match_face=True)
    entered_details = receive_details()

    is_match, distance = match_faces(image_of_id, face)
    extracted_text, preferences = manage_text_extractor(image_of_id)
    text_match_percentage, text_match, is_pass = manage_text_verification(preferences, extracted_text, entered_details)

    logger.info("Preparing Results...")
    result = {
        # text verification contributes to 40% of the total and face likeness for 60%
        "total_match": text_match_percentage*0.4 + distance*0.6,
        "text_match": text_match,
        "face_match": distance,
        "is_match": is_match,
        "is_pass": is_pass
    }
    return jsonify(result)


@verify.route('/verifyFaces', methods=['POST'])
def verify_faces():
    """
    Sample function to return a match percentage of an ID face image and
    picture of face.

    URL: http://localhost:5000/verifyFaces.

    """
    image_of_id, face = receive_faces(match_face=True)
    (is_match, distance) = match_faces(image_of_id, face)

    logger.info("Preparing Results...")
    result = {
        "face_match": distance,
        "is_match": is_match,
    }
    return jsonify(result)


@verify.route('/verifyInfo', methods=['POST'])
def verify_info():
    """
    Sample function to return a match percentage of an ID image and
    provided personal information.
    """
    image_of_id, _ = receive_faces(match_face=False)
    entered_details = receive_details()

    extracted_text, preferences = manage_text_extractor(image_of_id)
    text_match_percentage, text_match, is_pass = manage_text_verification(preferences, extracted_text, entered_details)

    logger.info("Preparing Results...")
    result = {
        "text_match": text_match,
        "is_pass": is_pass,
        "text_match_percentage": text_match_percentage
    }
    return jsonify(result)


def match_faces(image_of_id, face):
    """
    This function receives two images that receive images of faces that need to be verified.
    It is expected that an image of an ID and an image of a Profile picture will be received.
    Even if the expected images are not received the function will still apply a best effort solution.

    :param image_of_id (obj): An image of an ID that contains a face that needs to be verified.
    :param face (obj): A image of a face that needs to be verified.

    Returns:
        - boolean: Whether the two faces match (the distance between them is above the threshold value).
        - float: Return Euclidean distance between the vector representations of the two faces.

    """
    # Extract face
    face_detector = FaceDetector(SHAPE_PREDICTOR_PATH)
    extracted_face1 = face_detector.extract_face(image_of_id)
    extracted_face2 = face_detector.extract_face(face)

    # Verify faces
    face_verifier = FaceVerify(SHAPE_PREDICTOR_PATH, FACE_RECOGNITION_PATH)
    return face_verifier.verify(extracted_face1, extracted_face2)


def receive_faces(match_face=True):
    """
    This function receives faces/ID from request flask handler.
    The function checks for multiple means of receiving the faces/ID. These include

        - Receiving image by file path
        - Receiving image by URL
        - Receiving image by file Stream

    It is expected that an image of a face and an image of an ID will be sent.
    However, if the order is not followed that system will still be able to return the best effort result without
    loss of accuracy.

    :param match_face (boolean): Indicates if an additional profile of a face should be extracted.
            If an additional face should not be extracted simply return the ID image.

    Returns:
       - (obj): An image of a ID.
       - (obj): An image of a face if match_face is set to True.

    """
    data = {"success": False}
    # Get id image as numpy array
    # Check to see if an image was uploaded.
    if request.get_json().get("id_img", None) is not None:
        # Grab the uploaded image.
        image_of_id = grab_image(string=request.get_json()["id_img"])
    # Otherwise, assume that a URL was passed in.
    else:
        # Grab the URL from the request.
        url = request.get_json().get("url", None)
        # If the URL is None, then return an error.
        if url is None:
            data["error"] = "No URL provided."
            return jsonify(data)
            # Load the image and convert.
        image_of_id = grab_image(url=url)

    if not match_face:
        return image_of_id

    # Get face image as numpy array
    # Check to see if an image was uploaded.
    if request.get_json().get("face_img", None) is not None:
        # Grab the uploaded image.
        face = grab_image(string=request.get_json()["face_img"])
    # Otherwise, assume that a URL was passed in.
    else:
        # Grab the URL from the request.
        url = request.get_json().get("url", None)
        # If the URL is None, then return an error.
        if url is None:
            data["error"] = "No URL provided."
            return jsonify(data)
            # Load the image and convert.
        face = grab_image(url=url)

    return image_of_id, face


def manage_text_extractor(image_of_id):
    """
    This function manages the text extraction from an ID images.
    Management includes preparing text extraction preferences and receiving extracted text.

    :param image_of_id (obj): An image of an ID that text must be extracted from.

    Returns:
       - preferences (dict): Prepared list of preferences. May contain additional text extraction or logger preferences.
       - extracted_text (json object): A collection of text extracted from the ID.

    """
    preferences = {}
    # Grab additional parameters specifying techniques. Extract text
    logger.info("Setting Preferences")
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
    if 'verbose_verify' in request.get_json():
        preferences['verbose_verify'] = True if request.get_json()['verbose_verify'] == 'true' else False
    else:
        preferences['verbose_verify'] = False
    if 'useIO' in request.get_json():
        preferences['useIO'] = request.get_json()['useIO'] == 'true'

    extractor = TextExtractor(preferences)
    extracted_text = extractor.extract(image_of_id)
    return extracted_text, preferences


def manage_text_verification(preferences, extracted_text, entered_details):
    """
    The function manages the preparation before text verification and result of the text verification it self
    Management includes preparing logger functionality and controlling match percentages and messages.

    :param preferences (list): A list of preferences containing details about logger functionality.
    :param extracted_text (JSON object): Contains text extracted from ID image.
    :param entered_details (dict): Dictionary containing information that needs to be verified.

    Returns:
       - (float): Value representing the accuracy with which the entered details matches that of the extracted text.
       - (dict): Contains individual match percentages for different fields.
       - (boolean): Indicates if text_verification passes based on the threshold value.

    """
    text_verifier = TextVerify()
    verbose_verify = preferences['verbose_verify']
    logger.debug('%s text verifiction requested' % ('Verbose' if verbose_verify else 'Non-verbose'))
    (is_pass, text_match) = text_verifier.verify(extracted_text, entered_details, verbose=verbose_verify)
    # Check if we are working with verbose output for text verification
    text_match_percentage = text_match if not verbose_verify else text_match['total']
    return text_match_percentage, text_match, is_pass


def receive_details():
    """
    This function receives the details that need to be verified from the flask handler.

    Returns:
        - (dict): Details that need to be verified with that extracted from image.

    """
    entered_details = {
        "names": request.get_json()['names'],
        "surname": request.get_json()['surname'],
        "identity_number": request.get_json()['idNumber'],
        "nationality": request.get_json()['nationality'],
        "country_of_birth": request.get_json()['cob'],
        "status": request.get_json()['status'],
        "sex": request.get_json()['gender'],
        "date_of_birth": request.get_json()['dob']
    }
    return entered_details
