"""
----------------------------------------------------------------------
Authors: Stephan Nell
----------------------------------------------------------------------
Unit tests for the Thresholding Manager
----------------------------------------------------------------------
"""
import pytest
import numpy as np
from image_preprocessing.thresholding_manager import ThresholdingManager

# blank image to test with Height set 1 Width set at 1
blank_image = np.zeros((1, 1), dtype=np.uint8)


def test_thresholding_constructor_incorrect_type():
    """
    Test to see if constructor check for invalid type i.e not String type
    """
    with pytest.raises(TypeError):
        ThresholdingManager(123)


def test_thresholding_constructor_paramter_number():
    """
    Tests with incorrect number of parameters
    """
    with pytest.raises(TypeError):
        ThresholdingManager("adaptive", 1)


def test_thresholding_type():
    """
    Tests the verify function with a invalid Thresholding type
    """
    with pytest.raises(NameError):
        ThresholdingManager("Incorrect Thresholding type")


def test_thresholding_type_2():
    """
    Tests for adaptive thresholding passed to constructor
    """
    ThresholdingManager("adaptive")


def test_thresholding_type_3():
    """
    Tests for otsu thresholding passed to constructor
    """
    ThresholdingManager("otsu")


def test_thresholding_type_4():
    """
    Tests for missing parameter
    """
    with pytest.raises(TypeError):
        ThresholdingManager()


def test_thresholding_type_5():
    """
    Tests for Adaptive thresholding type passed as capital letter
    """
    ThresholdingManager("Adaptive")


def test_thresholding_type_6():
    """
    Tests for Otsu thresholding type passed as capital letter
    """
    ThresholdingManager("Otsu")


def test_apply():
    """
    Tests for apply function with Adaptive type
    """
    manager = ThresholdingManager("adaptive")
    manager.apply(blank_image)


def test_apply_2():
    """
    Tests for apply function with an invalid type used for thresholding
    """
    manager = ThresholdingManager("otsu")
    manager.thresholding_type = "Not a real type"
    with pytest.raises(NameError):
        manager.apply(blank_image)


def test_apply_3():
    """
    Tests for apply function with Otsu type
    """
    manager = ThresholdingManager("otsu")
    manager.apply(blank_image)


def test_apply_4():
    """
    Tests for apply function when invalid parameters passed
    """
    manager = ThresholdingManager("otsu")
    with pytest.raises(TypeError):
        manager.apply()


def test_apply_5():
    """
    For an image with a 1 by 1 dimension any thresholding will change to 255 colour value
    If function works correctly
    """
    manager = ThresholdingManager("otsu")
    assert manager.apply(blank_image) == 255


def test_otsu_thresholding():
    """
    Test Otsu thresholding with valid type will return 255 array for 1 by 1 dimension
    """
    manager = ThresholdingManager("otsu")
    assert manager.otsuThresholding(blank_image) == 255


def test_otsu_thresholding_2():
    """
    Test Otsu thresholding with invalid type String
    """
    manager = ThresholdingManager("otsu")
    with pytest.raises(TypeError):
        manager.otsuThresholding("A String invalid type")


def test_otsu_thresholding_3():
    """
    Test Otsu thresholding with invalid int
    """
    manager = ThresholdingManager("otsu")
    with pytest.raises(TypeError):
        manager.otsuThresholding(100)


def test_adaptive_thresholding():
    """
    Test adaptive thresholding with valid type will return 0 array for 1 by 1 dimension
    """
    manager = ThresholdingManager("adaptive")
    assert manager.adaptiveThresholding(blank_image) == 0


def test_adaptive_thresholding_2():
    """
    Test adaptive thresholding with invalid type String
    """
    manager = ThresholdingManager("adaptive")
    with pytest.raises(TypeError):
        manager.adaptiveThresholding("A String invalid type")


def test_adaptive_thresholding_3():
    """
    Test adaptive thresholding with invalid int
    """
    manager = ThresholdingManager("adaptive")
    with pytest.raises(TypeError):
        manager.adaptiveThresholding(100)
