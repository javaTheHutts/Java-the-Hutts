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
from hutts_verification.image_preprocessing.blur_manager import BlurManager

TEMPLATE_DIR = "{base_path}/../../main/python/hutts_verification/image_preprocessing/templates/".format(
    base_path=os.path.abspath(os.path.dirname(__file__)))

test_image_colour = cv2.imread(TEMPLATE_DIR + "temp_flag.jpg")


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
    manager = BlurManager("gaussian", (1, 1))
    assert manager.blur_type is "gaussian"
    assert manager.kernel_size == (1, 1)

def test_apply():
    """
    Test apply function with Gaussian
    """
    blur_manger = BlurManager("gaussian", [(7, 7)])
    blur_manger.apply(test_image_colour)
    assert blur_manger.blur_type is "gaussian"
    assert blur_manger.kernel_size == [(7, 7)]


def test_apply_2():
    """
    Test apply function with Median
    """
    blur_manger = BlurManager("median", [3])
    blur_manger.apply(test_image_colour)
    assert blur_manger.blur_type is "median"
    assert blur_manger.kernel_size == [3]


def test_apply_3():
    """
    Test apply function with Normal
    """
    blur_manger = BlurManager("normal", [(3, 3)])
    blur_manger.apply(test_image_colour)
    assert blur_manger.blur_type is "normal"
    assert blur_manger.kernel_size == [(3, 3)]


def test_apply_4():
    """
    Test apply function with Incorrect value
    """
    blur_manger = BlurManager("Mango", [(3, 3)])
    with pytest.raises(NameError):
        blur_manger.apply(test_image_colour)


def test_apply_5():
    """
    Test apply function with Invalid Blur kernel for Normal blur (Not a valid list)
    """
    blur_manger = BlurManager("normal", (3, 3))
    with pytest.raises(TypeError):
        blur_manger.apply(test_image_colour)


def test_apply_6():
    """
    Test apply function with Invalid Blur kernel for Normal blur (Not valid length)
    """
    blur_manger = BlurManager("normal", [(3, 3, 6)])
    with pytest.raises(ValueError):
        blur_manger.apply(test_image_colour)


def test_apply_7():
    """
    Test apply function with Invalid Blur kernel for Normal blur  (Not valid length)
    """
    blur_manger = BlurManager("normal", [3])
    with pytest.raises(TypeError):
        blur_manger.apply(test_image_colour)


def test_apply_8():
    """
    Test apply function with Invalid Blur kernel for Gaussian blur (Not a valid list)
    """
    blur_manger = BlurManager("gaussian", (3, 3))
    with pytest.raises(TypeError):
        blur_manger.apply(test_image_colour)


def test_apply_9():
    """
    Test apply function with Invalid Blur kernel for Gaussian blur (Not valid length)
    """
    blur_manger = BlurManager("gaussian", [(3, 3, 6)])
    with pytest.raises(ValueError):
        blur_manger.apply(test_image_colour)


def test_apply_10():
    """
    Test apply function with Invalid Blur kernel for Gaussian blur (Not valid length)
    """
    blur_manger = BlurManager("gaussian", [3])
    with pytest.raises(TypeError):
        blur_manger.apply(test_image_colour)


def test_apply_11():
    """
    Test apply function with Invalid Blur kernel for Median blur (Not a valid int)
    """
    blur_manger = BlurManager("median", ('A', 3))
    with pytest.raises(TypeError):
        blur_manger.apply(test_image_colour)


def test_apply_12():
    """
    Test apply function with Invalid Blur kernel for Median blur (Not of length 1)
    """
    blur_manger = BlurManager("median", (3, 3))
    with pytest.raises(ValueError):
        blur_manger.apply(test_image_colour)
