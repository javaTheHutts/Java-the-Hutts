"""
----------------------------------------------------------------------
Author: Nicolai van Niekerk
----------------------------------------------------------------------
Handles all requests relevant to the validation service of the API
----------------------------------------------------------------------
"""
from image_processing.sample_extract import TextExtractor
from image_preprocessing.face_manager import FaceDetector
from verification.text_verify import TextVerify
from verification.face_verify import FaceVerify
from flask import jsonify, request, Blueprint
from hutts_utils.hutts_logger import logger
from hutts_utils.image_handling import grab_image
from hutts_utils.pypath import correct_path
from pathlib import Path
from multiprocessing.pool import ThreadPool
import os


verify = Blueprint('verify', __name__)
pool = ThreadPool(processes=1)
THREAD_TIME_OUT = 7200

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
    ----------------------------------------------------------------------
    Authors: Nicolai van Niekerk, Stephan Nell, Marthinus Hermann
    ----------------------------------------------------------------------
    Sample function to return a match percentage of an ID image and
    provided personal information and picture of face
    ----------------------------------------------------------------------
    URL: http://localhost:5000/verifyID
    ----------------------------------------------------------------------
    """
    image_of_id, face = receive_faces(match_face=True)
    entered_details = receive_details()

    match_face_thread = pool.apply_async(match_faces, args=(image_of_id, face))

    # is_match, distance = match_faces(image_of_id, face)
    extracted_text, preferences = manage_text_extractor(image_of_id)
    text_match_percentage, text_match, is_pass = manage_text_verification(preferences, extracted_text, entered_details)

    logger.debug("Receiving match face thread results")
    is_match, distance = match_face_thread.get(THREAD_TIME_OUT)

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
        ----------------------------------------------------------------------
        Author: Nicolai van Niekerk, Stephan Nell
        ----------------------------------------------------------------------
        Sample function to return a match percentage of an ID face image and
        picture of face
        ----------------------------------------------------------------------
        URL: http://localhost:5000/verifyFaces
        ----------------------------------------------------------------------
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
        ----------------------------------------------------------------------
        Author: Nicolai van Niekerk, Stephan Nell
        ----------------------------------------------------------------------
        Sample function to return a match percentage of an ID image and
        provided personal information
        ----------------------------------------------------------------------
        URL: http://localhost:5000/verifyInfo
        ----------------------------------------------------------------------
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
    Author(s):
        Stephan Nell
    Args:
       image_of_id (:obj:'OpenCV image'): An image of an ID that contains a face that needs to be verified
       face (:obj:'OpenCV image'): A image of a face that needs to be verified
    Returns:
        bool: Represent if two faces indeed match True if distance calculated is
              below a threshold value. False if the distance calculated is above threshold value.
        float: Return Euclidean distance between the vector representation
               of the two faces
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
        Receiving image by file path
        Receiving image by URL
        Receiving image by file Stream
    It is expected that an image of a face and an image of an ID will be sent.
    However, if the order is not followed that system will still be able to return the best effort result without
    loss of accuracy.
    Author(s):
        Stephan Nell
    Args:
        match_face (bool): Indicates if additional profile of a face should be extracted.
            If an additional face should not be extracted simply return the ID image.
    Returns:
       image_of_id (:obj:'OpenCV image'): An image of a ID.
       face (:obj:'OpenCV image'): An image of a face. If match_face is set to True
    """
    data = {"success": False}
    # Get id image as numpy array
    # Check to see if an image was uploaded.
    if request.files.get("id_img", None) is not None:
        # Grab the uploaded image.
        image_of_id = grab_image(stream=request.files["id_img"])
    # Otherwise, assume that a URL was passed in.
    else:
        # Grab the URL from the request.
        url = request.args.get("url", None)
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
    if request.files.get("face_img", None) is not None:
        # Grab the uploaded image.
        face = grab_image(stream=request.files["face_img"])
    # Otherwise, assume that a URL was passed in.
    else:
        # Grab the URL from the request.
        url = request.args.get("url", None)
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
    Author(s):
        Stephan Nell
    Args:
       image_of_id (:obj:'OpenCV image'): An image of an ID that text must be extracted from.
    Returns:
       preferences (dict): Prepared list of preferences. May contained additional text extraction or logger preferences.
       extracted_text (json object): A collection of text extracted from the ID.
    """
    preferences = {}
    # Grab additional parameters specifying techniques. Extract text
    logger.info("Setting Preferences")
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
    if 'verbose_verify' in request.form:
        preferences['verbose_verify'] = True if request.form['verbose_verify'] == 'true' else False
    else:
        preferences['verbose_verify'] = False
    if 'useIO' in request.form:
        preferences['useIO'] = request.form['useIO'] == 'true'

    extractor = TextExtractor(preferences)
    extracted_text = extractor.extract(image_of_id)
    return extracted_text, preferences


def manage_text_verification(preferences, extracted_text, entered_details):
    """
    The function manages the preparation before text verification and result of the text verification it self
    Management includes preparing logger functionality and controlling match percentages and messages.
    Author(s):
        Stephan Nell
    Args:
        preferences (list): A list of preferences. Containing details about logger functionality.
        extracted_text (JSON object): Contains text extracted from ID image.
        entered_details (dict): Dictionary containing information that needs to be verified
    Returns:
       text_match_percentage (float): Value representing the accuracy with which the entered details
            matches that of the extracted text.
       text_match (dict): Contains intermediate match percentages for different details.
            For Example the match percentage between just the date_of_birth fields
       is_pass (bool): Indicates if text_verification passes.
            If match percentage is above threshold provided in preferences then verification passes.
            If match percentage is below threshold value provided in preferences then verification fails.
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
    Author(s):
        Stephan Nell
    Returns:
        entered_details (dict): Details that need to be verified with that extracted from image.
    """
    entered_details = {
        "names": request.form['names'],
        "surname": request.form['surname'],
        "identity_number": request.form['idNumber'],
        "nationality": request.form['nationality'],
        "country_of_birth": request.form['cob'],
        "status": request.form['status'],
        "sex": request.form['gender'],
        "date_of_birth": request.form['dob']
    }
    return entered_details
