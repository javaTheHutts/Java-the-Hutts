"""
----------------------------------------------------------------------
Author: Nicolai van Niekerk
----------------------------------------------------------------------
Handles all requests relevant to the validation service of the API
----------------------------------------------------------------------
"""
import cv2
import numpy as np
from imutils.convenience import url_to_image
from image_processing.sample_extract import TextExtractor
from image_preprocessing.face_manager import FaceDetector
from verification.text_verify import TextVerify
from verification.face_verify import FaceVerify
from flask import jsonify, request, Blueprint
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
        Author: Nicolai van Niekerk
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
        image_of_id = _grab_image(stream=request.files["id_img"])
    # Otherwise, assume that a URL was passed in.
    else:
        # Grab the URL from the request.
        url = request.args.get("url", None)
        # If the URL is None, then return an error.
        if url is None:
            data["error"] = "No URL provided."
            return jsonify(data)
            # Load the image and convert.
        image_of_id = _grab_image(url=url)

    # Get face image as numpy array
    # Check to see if an image was uploaded.
    if request.files.get("face_img", None) is not None:
        # Grab the uploaded image.
        face = _grab_image(stream=request.files["face_img"])
    # Otherwise, assume that a URL was passed in.
    else:
        # Grab the URL from the request.
        url = request.args.get("url", None)
        # If the URL is None, then return an error.
        if url is None:
            data["error"] = "No URL provided."
            return jsonify(data)
            # Load the image and convert.
        face = _grab_image(url=url)

    entered_details = {
        "names": request.form['names'], "surname": request.form['surname'], "identity_number":
        request.form['idNumber'], "nationality": request.form['nationality'], "country_of_birth":
        request.form['cob'], "status": request.form['status'], "sex": request.form['gender'], "date_of_birth":
        request.form['dob']
    }

    # Extract face
    face_detector = FaceDetector(SHAPE_PREDICTOR_PATH)
    gray_extracted_face1 = face_detector.face_likeness_extraction(image_of_id)
    gray_extracted_face2 = face_detector.face_likeness_extraction(face)

    # Verify faces
    face_verifier = FaceVerify(SHAPE_PREDICTOR_PATH, FACE_RECOGNITION_PATH)
    (isMatch, distance) = face_verifier.verify(gray_extracted_face1, gray_extracted_face2)

    # Extract text
    preferences = {}
    extractor = TextExtractor(preferences)
    extracted_text = extractor.extract(image_of_id)

    # Verify text
    text_verifier = TextVerify()
    (isPass, text_match_percentage) = text_verifier.verify(extracted_text, entered_details)

    result = {
        "total_match": 95,
        "text_match": text_match_percentage,
        "face_match": distance
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
