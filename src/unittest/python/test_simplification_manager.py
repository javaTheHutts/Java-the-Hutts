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

TEMPLATE_DIR = "{base_path}/../../main/python/image_preprocessing/templates/temp_flag.jpg".format(
    base_path=os.path.abspath(os.path.dirname(__file__)))
test_image_colour = cv2.imread(TEMPLATE_DIR)

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

def test_perspective_type():
    """
    Tests if incorrect type i.e not Num array will be rejected
    """
    simp_manager = SimplificationManager()
    with pytest.raises(TypeError):
        simp_manager.perspectiveTransformation(1)

def test_perspective_thresholding():
    """
    Tests perspective thresholding
    """
    # disable multi-threading in OpenCV for main thread to avoid problems after fork
    cv2.setNumThreads(0)
    simp_manager = SimplificationManager()
    simp_manager.perspectiveTransformation(test_image_colour)
    # enable multi-threading in OpenCV for child thread
    cv2.setNumThreads(-1)