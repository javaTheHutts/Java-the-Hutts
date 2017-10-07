"""
----------------------------------------------------------------------
Authors: Stephan Nell
----------------------------------------------------------------------
Unit tests for the Simplification Manager
----------------------------------------------------------------------
"""
import pytest
import numpy as np
import cv2
import os
from image_processing.simplification_manager import SimplificationManager

# blank image to test with Height set 1 Width set at 1
blank_image = np.zeros((1, 1), dtype=np.uint8)

TEMPLATE_DIR = "{base_path}/../../main/python/image_preprocessing/templates/".format(
    base_path=os.path.abspath(os.path.dirname(__file__)))

test_image_colour = cv2.imread(TEMPLATE_DIR + "temp_flag.jpg")

thanks_obama = cv2.imread(TEMPLATE_DIR + "obama.jpg")

# Soap Joe official example for Fraud Detection for South African ID books
soap_joe = cv2.imread(TEMPLATE_DIR + "soapJoeExample.jpg")


def test_simplification_constructor():
    """
    Tests with no parameters
    """
    SimplificationManager()


def test_simplification_constructor_1():
    """
    Tests with incorrect number of parameters
    """
    with pytest.raises(TypeError):
        SimplificationManager(1)


def test_perspective_transform():
    """
    Tests with no parameters
    """
    simp_manager = SimplificationManager()
    with pytest.raises(TypeError):
        simp_manager.perspectiveTransformation()


def test_perspective_transform_2():
    """
    Tests with incorrect number of parameters
    """
    simp_manager = SimplificationManager()
    with pytest.raises(TypeError):
        simp_manager.perspectiveTransformation(blank_image, 1)


def test_perspective_transform_3():
    """
    Tests perspective thresholding and transformation with plain colour image
    """
    # disable multi-threading in OpenCV for main thread to avoid problems after fork
    cv2.setNumThreads(0)
    simp_manager = SimplificationManager()
    img = simp_manager.perspectiveTransformation(test_image_colour)
    assert np.array_equal(test_image_colour, img)
    cv2.setNumThreads(-1)


def test_perspective_transform_4():
    """
    Tests perspective thresholding and transformation with soap joe book type
    """
    # disable multi-threading in OpenCV for main thread to avoid problems after fork
    cv2.setNumThreads(0)
    simp_manager = SimplificationManager()
    img = simp_manager.perspectiveTransformation(soap_joe)
    assert np.array_equal(soap_joe, img)
    # enable multi-threading in OpenCV for child thread
    cv2.setNumThreads(-1)


def test_perspective_transform_5():
    """
    Tests perspective thresholding and transformation with Obama not card type
    """
    # disable multi-threading in OpenCV for main thread to avoid problems after fork
    cv2.setNumThreads(0)
    simp_manager = SimplificationManager()
    img = simp_manager.perspectiveTransformation(thanks_obama)
    assert np.array_equal(thanks_obama, img)
    # enable multi-threading in OpenCV for child thread
    cv2.setNumThreads(-1)


def test_perspective_type():
    """
    Tests if incorrect type i.e not Num array will be rejected
    """
    simp_manager = SimplificationManager()
    with pytest.raises(TypeError):
        simp_manager.perspectiveTransformation(1)
