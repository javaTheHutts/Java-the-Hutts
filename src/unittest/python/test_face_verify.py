"""
----------------------------------------------------------------------
Authors: Stephan Nell
----------------------------------------------------------------------
Unit tests for the Face Verify
All the images used are from public domain and are copyright free
----------------------------------------------------------------------
"""
import pytest
import cv2
import os
from verification.face_verify import FaceVerify
from image_preprocessing.blur_manager import BlurManager

# Constants path to trained data for Shape Predictor.
SHAPE_PREDICTOR_PATH = "{base}/../../main/python/image_preprocessing/trained_data/shape_predictor_face_landmarks.dat".format(
    base=os.path.abspath(os.path.dirname(__file__)))

FACE_RECOGNITION_PATH = "{base}/../../main/python/image_preprocessing/trained_data/dlib_face_recognition_resnet_model_v1.dat".format(
    base=os.path.abspath(os.path.dirname(__file__)))

TEMPLATE_DIR = "{base_path}/../../main/python/image_preprocessing/templates/".format(
    base_path=os.path.abspath(os.path.dirname(__file__)))

test_image_colour = cv2.imread(TEMPLATE_DIR + "temp_flag.jpg")

thanks_obama = cv2.imread(TEMPLATE_DIR + "obama.jpg")

# Soap Joe official example for Fraud Detection for South African ID books
soap_joe = cv2.imread(TEMPLATE_DIR + "soapJoeExample.jpg")


def test_face_verify_constructor():
    """
    Test to see if constructor without path passed
    """
    with pytest.raises(TypeError):
        FaceVerify()


def test_face_verify_constructor_2():
    """
    Test to see if constructor with one path passed and other omitted
    """
    with pytest.raises(TypeError):
        FaceVerify(SHAPE_PREDICTOR_PATH)


def test_face_verify_constructor_3():
    """
    Test to see if constructor one path and one incorrect type
    """
    with pytest.raises(TypeError):
        FaceVerify(SHAPE_PREDICTOR_PATH, 1)


def test_face_verify_constructor_4():
    """
    Test to see if constructor one path and one incorrect type
    """
    with pytest.raises(TypeError):
        FaceVerify(1, FACE_RECOGNITION_PATH)


def test_face_verify_constructor_5():
    """
    Test to see if constructor both paths incorrect
    """
    with pytest.raises(TypeError):
        FaceVerify(1, FACE_RECOGNITION_PATH)


def test_face_verify_constructor_6():
    """
    Test to see if constructor both paths correct
    """
    FaceVerify(SHAPE_PREDICTOR_PATH, FACE_RECOGNITION_PATH)


def test_face_verify():
    """
    Test with no value provided
    """
    face_verf = FaceVerify(SHAPE_PREDICTOR_PATH, FACE_RECOGNITION_PATH)
    with pytest.raises(TypeError):
        face_verf.verify()


def test_face_verify_2():
    """
    Test with one correct value provided
    """
    face_verf = FaceVerify(SHAPE_PREDICTOR_PATH, FACE_RECOGNITION_PATH)
    with pytest.raises(TypeError):
        face_verf.verify(test_image_colour)


def test_face_verify_3():
    """
    Test with one correct value provided
    """
    face_verf = FaceVerify(SHAPE_PREDICTOR_PATH, FACE_RECOGNITION_PATH)
    with pytest.raises(TypeError):
        face_verf.verify(test_image_colour)


def test_face_verify_4():
    """
    Test with correct value provided but with no face
    """
    face_verf = FaceVerify(SHAPE_PREDICTOR_PATH, FACE_RECOGNITION_PATH)
    with pytest.raises(ValueError):
        face_verf.verify(test_image_colour, test_image_colour)


def test_face_verify_5():
    """
    Test with one correct value provided but only one face is correct
    """
    face_verf = FaceVerify(SHAPE_PREDICTOR_PATH, FACE_RECOGNITION_PATH)
    with pytest.raises(ValueError):
        face_verf.verify(face1=thanks_obama, face2=test_image_colour)


def test_face_verify_6():
    """
    Test with one correct value provided with both faces correct must be 100% since it is the same face
    """
    face_verf = FaceVerify(SHAPE_PREDICTOR_PATH, FACE_RECOGNITION_PATH)
    face_verf.verify(thanks_obama, thanks_obama)


def test_face_verify_7():
    """
    Provides different faces to verification module.
    Face should return a low result percentage.
    """
    face_verf = FaceVerify(SHAPE_PREDICTOR_PATH, FACE_RECOGNITION_PATH)
    face_verf.verify(thanks_obama, soap_joe)


def test_face_verify_8():
    """
    Test with the same face for both images.
    One of the images will be slightly damage.
    The  damage test is to establish if the face verification can compensate for lower quality images.
    """
    face_verf = FaceVerify(SHAPE_PREDICTOR_PATH, FACE_RECOGNITION_PATH)
    blur_manager = BlurManager("median", [7])
    damaged_obama = thanks_obama.copy()
    damaged_obama = blur_manager.apply(damaged_obama)
    face_verf.verify(thanks_obama, damaged_obama)
