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
import numpy as np
from hutts_verification.utils.image_handling import grab_image

TEMPLATE_DIR = "{base_path}/../../main/python/hutts_verification/image_preprocessing/templates/".format(
    base_path=os.path.abspath(os.path.dirname(__file__)))

test_image_colour = cv2.imread(TEMPLATE_DIR + "temp_flag.jpg")

# Face that is not fully aligned with the center of the image.
obama_skew = cv2.imread(TEMPLATE_DIR + "obamaSkew.jpg")



def test_grab_image():
    """
    Test image handling with no paramters
    """
    with pytest.raises(ValueError):
        grab_image()


@pytest.mark.skip(reason="Need Stable Internet Connection to test")
def test_grab_image_2():
    """
    Test image handling with url
    """
    test_path_image = grab_image(url="http://www.pyimagesearch.com/wp-content/uploads/2015/05/obama.jpg")
    assert np.array_equal(obama_skew, test_path_image)


def test_grab_image_3():
    """
    Test image handling with path specified
    """
    test_path_image = grab_image(path=TEMPLATE_DIR + "temp_flag.jpg")
    assert np.array_equal(test_image_colour, test_path_image)


def test_grab_image_4():
    """
    Test image handling with incorrect path specified
    """
    with pytest.raises(ValueError):
        grab_image(path=TEMPLATE_DIR + "temp_flagg.jpg")


def test_grab_image_5():
    """
    Test image handling stream with incorrect Attribute type
    """
    with pytest.raises(AttributeError):
        grab_image(stream=TEMPLATE_DIR + "temp_flagg.jpg")


def test_grab_image_6():
    """
    Test image handling with path specified
    """
    test_path_image = grab_image(path=TEMPLATE_DIR + "temp_flag.jpg")
    with pytest.raises(AttributeError):
        grab_image(stream=test_path_image)

