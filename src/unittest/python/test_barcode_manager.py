"""
----------------------------------------------------------------------
Authors: Stephan Nell
----------------------------------------------------------------------
Unit tests for the Barcode Manager
----------------------------------------------------------------------
"""
import pytest
import numpy as np
import cv2
import os
from image_processing.barcode_manager import BarCodeManager

# blank image to test with Height set 1 Width set at 1
blank_image = np.zeros((1, 1), dtype=np.uint8)

TEMPLATE_DIR = "{base_path}/../../main/python/image_preprocessing/templates/".format(
    base_path=os.path.abspath(os.path.dirname(__file__)))
test_image_colour = cv2.imread(TEMPLATE_DIR + "pp2.jpg")
thanks_obama = cv2.imread(TEMPLATE_DIR + "obama.jpg")
# Soap Joe official example for Fraud Detection for South African ID books
soap_joe = cv2.imread(TEMPLATE_DIR + "soapJoeExample.jpg")

cv2 = pytest.importorskip("cv2")


def test_barcode_detect():
    """
    Tests with wrong parameters
    """
    bar_manager = BarCodeManager()
    with pytest.raises(TypeError):
        bar_manager.detect(12)


def test_barcode_detect_2():
    """
    Tests with no parameters
    """
    bar_manager = BarCodeManager()
    with pytest.raises(TypeError):
        bar_manager.detect()


def test_barcode_detect_3():
    """
    Tests with correct parameters but with no barcode
    """
    cv2.setNumThreads(0)
    bar_manager = BarCodeManager()
    bar_manager.detect(test_image_colour)
    cv2.setNumThreads(-1)


def test_barcode_detect_4():
    """
    Tests with correct parameters but with no barcode
    """
    cv2.setNumThreads(0)
    bar_manager = BarCodeManager()
    bar_manager.detect(thanks_obama)
    cv2.setNumThreads(-1)


def test_barcode_detect_5():
    """
    Tests with correct parameters with barcode
    """
    cv2.setNumThreads(0)
    bar_manager = BarCodeManager()
    bar_manager.detect(soap_joe)
    cv2.setNumThreads(-1)


def test_get_barcode():
    """
    Test get barcode with no barcode present
    """
    cv2.setNumThreads(0)
    bar_manager = BarCodeManager()
    bar_manager.get_barcode_info(thanks_obama)
    cv2.setNumThreads(-1)


def test_get_barcode_2():
    """
    Test get barcode with barcode present
    """
    cv2.setNumThreads(0)
    bar_manager = BarCodeManager()
    bar_manager.get_barcode_info(soap_joe)
    cv2.setNumThreads(-1)


def test_get_barcode_3():
    """
    Test get barcode with barcode present but damaged
    """
    cv2.setNumThreads(0)
    bar_manager = BarCodeManager()
    (_, _, box) = bar_manager.detect(soap_joe)
    soap_joe_damaged = bar_manager.apply_barcode_blur(soap_joe, box)
    bar_manager.get_barcode_info(soap_joe_damaged)
    cv2.setNumThreads(-1)


def test_apply_barcode_blur():
    """
    Tests with correct parameters but with no barcode to blur
    """
    cv2.setNumThreads(0)
    bar_manager = BarCodeManager()
    (_, _, box) = bar_manager.detect(thanks_obama)
    bar_manager.apply_barcode_blur(thanks_obama, box)
    cv2.setNumThreads(-1)
