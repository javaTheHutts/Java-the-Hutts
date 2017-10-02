"""
----------------------------------------------------------------------
Authors: Stephan Nell
----------------------------------------------------------------------
Unit tests for the Blur Manager
----------------------------------------------------------------------
"""
import pytest
import cv2
import os
from image_preprocessing.blur_manager import BlurManager

TEMPLATE_DIR = "{base_path}/../../main/python/image_preprocessing/templates/temp_flag.jpg".format(
    base_path=os.path.abspath(os.path.dirname(__file__)))
test_image_colour = cv2.imread(TEMPLATE_DIR)


def test_thresholding_constructor_incorrect_type():
    """
    Test to see if constructor check for invalid type i.e not String type
    """
    with pytest.raises(TypeError):
        BlurManager(1, (1, 1))


def test_thresholding_constructor_correct_type():
    """
    Test to see if constructor valid type
    """
    BlurManager("gaussian", (1, 1))


def test_apply():
    """
    Test apply function with Gaussian
    """
    blur_manger = BlurManager("gaussian", [(7, 7)])
    blur_manger.apply(test_image_colour)


def test_apply_2():
    """
    Test apply function with Median
    """
    blur_manger = BlurManager("median", [3])
    blur_manger.apply(test_image_colour)


def test_apply_3():
    """
    Test apply function with Normal
    """
    blur_manger = BlurManager("normal", [(3, 3)])
    blur_manger.apply(test_image_colour)


def test_apply_4():
    """
    Test apply function with Incorrect value
    """
    blur_manger = BlurManager("Mango", [(3, 3)])
    with pytest.raises(NameError):
        blur_manger.apply(test_image_colour)
