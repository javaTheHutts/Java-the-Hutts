"""
----------------------------------------------------------------------
Authors: Stephan Nell
----------------------------------------------------------------------
Unit tests for the Image Handling
----------------------------------------------------------------------
"""
import pytest
import cv2
import os
from hutts_utils.image_handling import grab_image

TEMPLATE_DIR = "{base_path}/../../main/python/image_preprocessing/templates/temp_flag.jpg".format(
    base_path=os.path.abspath(os.path.dirname(__file__)))
test_image_colour = cv2.imread(TEMPLATE_DIR)

def test_grab_image():
    """
    Test image handling with no paramters
    """
    with pytest.raises(ValueError):
        grab_image()

def test_grab_image_2():
    """
    Test image handling with url
    """
    grab_image(url="http://www.pyimagesearch.com/wp-content/uploads/2015/05/obama.jpg")

def test_grab_image_3():
    """
    Test image handling with url
    """
    grab_image(path=TEMPLATE_DIR)


