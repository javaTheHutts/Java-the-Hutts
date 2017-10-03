"""
----------------------------------------------------------------------
Authors: Stephan Nell
----------------------------------------------------------------------
Unit tests for the Color Manager
----------------------------------------------------------------------
"""
import pytest
import cv2
import os
from image_preprocessing.color_manager import ColorManager

TEMPLATE_DIR = "{base_path}/../../main/python/image_preprocessing/templates/".format(
    base_path=os.path.abspath(os.path.dirname(__file__)))

test_image_colour = cv2.imread(TEMPLATE_DIR + "temp_flag.jpg")
thanks_obama = cv2.imread(TEMPLATE_DIR + "obama.jpg")


def test_color_manager_constructor():
    """
    Test constructor without any parameters
    """
    with pytest.raises(TypeError):
        ColorManager()


def test_color_manager_apply():
    """
    Test Color manager apply extract type
    """
    manager = ColorManager("extract", "red", (17, 7))
    manager.apply(test_image_colour)


def test_color_manager_apply_2():
    """
    Test Color manager apply histogram Equalisation type
    """
    manager = ColorManager("histogram")
    manager.apply(thanks_obama)


def test_color_manager_apply_3():
    """
    Test Color manager apply Black hat Morph type
    """
    manager = ColorManager("blackHat", "green")
    manager.apply(test_image_colour)


def test_color_manager_apply_4():
    """
    Test Color manager apply Top hat Morph type
    """
    manager = ColorManager("topHat", "red_blue")
    manager.apply(test_image_colour)


def test_color_manager_apply_5():
    """
    Test Color manager apply White hat Morph type
    """
    manager = ColorManager("whiteHat", "blue")
    manager.apply(test_image_colour)


def test_color_manager_apply_6():
    """
    Test Color manager apply with incorrect value
    """
    manager = ColorManager("Extracttttt", "blue")
    with pytest.raises(NameError):
        manager.apply(test_image_colour)


def test_color_manager_apply_extract():
    """
    Test Extract Colour with Blue
    """
    manager = ColorManager("extract", "blue", (17, 7))
    manager.apply(test_image_colour)


def test_color_manager_apply_extract_2():
    """
    Test Extract Colour with Green
    """
    manager = ColorManager("extract", "green")
    manager.apply(test_image_colour)


def test_color_manager_apply_extract_3():
    """
    Test Extract Colour with Red
    """
    manager = ColorManager("extract", "red")
    manager.apply(test_image_colour)


def test_color_manager_apply_extract_4():
    """
    Test Extract Colour with red_blue
    """
    manager = ColorManager("extract", "red_blue")
    manager.apply(test_image_colour)


def test_color_manager_apply_extract_5():
    """
    Test Extract Colour with green_blue
    """
    manager = ColorManager("extract", "green_blue")
    manager.apply(test_image_colour)


def test_color_manager_apply_extract_6():
    """
    Test Extract Colour with green_red
    """
    manager = ColorManager("extract", "green_red")
    manager.apply(test_image_colour)


def test_color_manager_apply_extract_7():
    """
    Test Extract Colour with incorrect value
    """
    manager = ColorManager("extract", "red_purple")
    with pytest.raises(NameError):
        manager.apply(test_image_colour)
