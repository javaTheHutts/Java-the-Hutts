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
import os


verify = Blueprint('verify', __name__)

# Constants path to trained data for Shape Predictor.
SHAPE_PREDICTOR_PATH = "{base_path}/../image_preprocessing/trained_data/shape_predictor_face_landmarks.dat".format(
    base_path=os.path.abspath(os.path.dirname(__file__)))

FACE_RECOGNITION_PATH = "{base}/../image_preprocessing/trained_data/dlib_face_recognition_resnet_model_v1.dat".format(
                                            base=os.path.abspath(os.path.dirname(__file__)))


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

    # Extract face
    face_detector = FaceDetector(SHAPE_PREDICTOR_PATH)
    extracted_face1, _ = face_detector.extract_face(image_of_id)
    extracted_face2, _ = face_detector.extract_face(face)

    # Verify faces
    face_verifier = FaceVerify(SHAPE_PREDICTOR_PATH, FACE_RECOGNITION_PATH)
    (is_match, distance) = face_verifier.verify(extracted_face1, extracted_face2)

    # Extract text
    # Grab additional parameters specifying techniques
    preferences = {}
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

    extractor = TextExtractor(preferences)
    extracted_text = extractor.extract(image_of_id)

    # Verify text
    text_verifier = TextVerify()
    (is_pass, text_match_percentage) = text_verifier.verify(extracted_text, entered_details)

    logger.info("Preparing Results...")
    result = {
        # text verification contributes to 40% of the total and face likeness for 60%
        "total_match": text_match_percentage*0.4 + distance*0.6,
        "text_match": text_match_percentage,
        "face_match": distance,
        "is_match": is_match,
        "is_pass": is_pass
    }
    return jsonify(result)


@verify.route('/verifyFaces', methods=['POST'])
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


@verify.route('/verifyInfo', methods=['POST'])
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
