"""
----------------------------------------------------------------------
Authors: Stephan Nell
----------------------------------------------------------------------
Unit tests for the Blur Manager
----------------------------------------------------------------------
"""
import pytest
import numpy as np
import cv2
import os
from image_preprocessing.blur_manager import BlurManager

# blank image to test with Height set 1 Width set at 1
blank_image = np.zeros((1, 1), dtype=np.uint8)

TEMPLATE_DIR = "{base_path}/../../main/python/image_preprocessing/templates/temp_flag.jpg".format(
    base_path=os.path.abspath(os.path.dirname(__file__)))
test_image_colour = cv2.imread(TEMPLATE_DIR)

def test_thresholding_constructor_incorrect_type():
    """
    Test to see if constructor check for invalid type i.e not String type
    """
    with pytest.raises(TypeError):
        BlurManager(1, (1,1))

def test_thresholding_constructor_correct_type():
    """
    Test to see if constructor valid type
    """
    BlurManager("gaussian", (1,1))

def test_apply():
    """
    Test apply function with Gaussian
    """
    blurmanger = BlurManager("gaussian", [(7, 7)])
    blurmanger.apply(test_image_colour)

def test_apply_2():
    """
    Test apply function with Median
    """
    blurmanger = BlurManager("median", [3])
    blurmanger.apply(test_image_colour)

def test_apply_3():
    """
    Test apply function with Normal
    """
    blurmanger = BlurManager("normal", [(3, 3)])
    blurmanger.apply(test_image_colour)

def test_apply_4():
    """
    Test apply function with Median
    """
    blurmanger = BlurManager("Mango", [(3, 3)])
    with pytest.raises(NameError):
        blurmanger.apply(test_image_colour)
