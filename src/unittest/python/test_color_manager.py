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
    cv2.setNumThreads(0)
    manager = ColorManager("extract", "red", (17, 7))
    manager.apply(test_image_colour)
    assert manager.channel is "red"
    assert manager.kernel_size == (17, 7)
    assert manager.color_extraction_type is "extract"
    cv2.setNumThreads(-1)


def test_color_manager_apply_2():
    """
    Test Color manager apply histogram Equalisation type
    """
    cv2.setNumThreads(0)
    manager = ColorManager("histogram")
    manager.apply(thanks_obama)
    assert manager.channel is "green"
    assert manager.kernel_size == (13, 7)
    assert manager.color_extraction_type is "histogram"
    cv2.setNumThreads(-1)


def test_color_manager_apply_3():
    """
    Test Color manager apply Black hat Morph type
    """
    cv2.setNumThreads(0)
    manager = ColorManager("blackHat", "green")
    manager.apply(test_image_colour)
    assert manager.channel is "green"
    assert manager.kernel_size == (13, 7)
    assert manager.color_extraction_type is "blackHat"
    cv2.setNumThreads(-1)


def test_color_manager_apply_4():
    """
    Test Color manager apply Top hat Morph type
    """
    cv2.setNumThreads(0)
    manager = ColorManager("topHat", "red_blue")
    manager.apply(test_image_colour)
    assert manager.channel is "red_blue"
    assert manager.kernel_size == (13, 7)
    assert manager.color_extraction_type is "topHat"
    cv2.setNumThreads(-1)


def test_color_manager_apply_5():
    """
    Test Color manager apply White hat Morph type
    """
    cv2.setNumThreads(0)
    manager = ColorManager("whiteHat", "blue")
    manager.apply(test_image_colour)
    assert manager.channel is "blue"
    assert manager.kernel_size == (13, 7)
    assert manager.color_extraction_type is "whiteHat"
    cv2.setNumThreads(-1)


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
    cv2.setNumThreads(0)
    manager = ColorManager("extract", "blue", (17, 7))
    manager.apply(test_image_colour)
    assert manager.channel is "blue"
    assert manager.kernel_size == (17, 7)
    assert manager.color_extraction_type is "extract"
    cv2.setNumThreads(-1)


def test_color_manager_apply_extract_2():
    """
    Test Extract Colour with Green
    """
    cv2.setNumThreads(0)
    manager = ColorManager("extract", "green")
    manager.apply(test_image_colour)
    assert manager.channel is "green"
    assert manager.kernel_size == (13, 7)
    assert manager.color_extraction_type is "extract"
    cv2.setNumThreads(-1)


def test_color_manager_apply_extract_3():
    """
    Test Extract Colour with Red
    """
    cv2.setNumThreads(0)
    manager = ColorManager("extract", "red")
    manager.apply(test_image_colour)
    assert manager.channel is "red"
    assert manager.kernel_size == (13, 7)
    assert manager.color_extraction_type is "extract"
    cv2.setNumThreads(-1)


def test_color_manager_apply_extract_4():
    """
    Test Extract Colour with red_blue
    """
    cv2.setNumThreads(0)
    manager = ColorManager("extract", "red_blue")
    manager.apply(test_image_colour)
    assert manager.channel is "red_blue"
    assert manager.kernel_size == (13, 7)
    assert manager.color_extraction_type is "extract"
    cv2.setNumThreads(-1)


def test_color_manager_apply_extract_5():
    """
    Test Extract Colour with green_blue
    """
    cv2.setNumThreads(0)
    manager = ColorManager("extract", "green_blue")
    manager.apply(test_image_colour)
    assert manager.channel is "green_blue"
    assert manager.kernel_size == (13, 7)
    assert manager.color_extraction_type is "extract"
    cv2.setNumThreads(-1)


def test_color_manager_apply_extract_6():
    """
    Test Extract Colour with green_red
    """
    cv2.setNumThreads(0)
    manager = ColorManager("extract", "green_red")
    manager.apply(test_image_colour)
    assert manager.channel is "green_red"
    assert manager.kernel_size == (13, 7)
    assert manager.color_extraction_type is "extract"
    cv2.setNumThreads(-1)


def test_color_manager_apply_extract_7():
    """
    Test Extract Colour with incorrect value
    """
    manager = ColorManager("extract", "red_purple")
    with pytest.raises(NameError):
        manager.apply(test_image_colour)


def test_color_manager_apply_extract_8():
    """
    Test Extract Colour with incorrect value for Blackhat extraction (Invalid Type)
    """
    manager = ColorManager("blackHat", "blue", 'a')
    with pytest.raises(TypeError):
        manager.apply(test_image_colour)


def test_color_manager_apply_extract_9():
    """
    Test Extract Colour with incorrect value for blackhat extraction.
    """
    manager = ColorManager("blackHat", "blue", (1, 3, 4, 5))
    with pytest.raises(ValueError):
        manager.apply(test_image_colour)


def test_color_manager_apply_extract_10():
    """
    Test Extract Colour with incorrect value for topHat (Invalid Type)
    """
    manager = ColorManager("topHat", "blue", 'a')
    with pytest.raises(TypeError):
        manager.apply(test_image_colour)


def test_color_manager_apply_extract_11():
    """
    Test Extract Colour with incorrect value for Tophat extraction
    """
    manager = ColorManager("topHat", "blue", (1, 3, 4, 5))
    with pytest.raises(ValueError):
        manager.apply(test_image_colour)