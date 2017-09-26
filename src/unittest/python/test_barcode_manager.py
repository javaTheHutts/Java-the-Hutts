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

cv2 = pytest.importorskip("cv2")

def test_barcode_detect():
    """
    Tests with wrong paramters
    """
    bar_manager = BarCodeManager()
    with pytest.raises(TypeError):
        bar_manager.detect(12)

def test_barcode_detect_2():
    """
    Tests with no paramters
    """
    bar_manager = BarCodeManager()
    with pytest.raises(TypeError):
        bar_manager.detect()

def test_barcode_detect_3():
    """
    Tests with correct parameters but with no barcodes
    """
    cv2.setNumThreads(0)
    bar_manager = BarCodeManager()
    bar_manager.detect(test_image_colour)
    cv2.setNumThreads(-1)

def test_barcode_detect_4():
    """
    Tests with correct parameters but with no barcodes
    """
    cv2.setNumThreads(0)
    bar_manager = BarCodeManager()
    bar_manager.detect(thanks_obama)
    cv2.setNumThreads(-1)

def test_get_barcode():
    """
    Tests with correct parameters but with no barcodes
    """
    cv2.setNumThreads(0)
    bar_manager = BarCodeManager()
    bar_manager.get_barcode_info(thanks_obama)
    cv2.setNumThreads(-1)

def test_apply_barcode_blur():
    """
    Tests with correct parameters but with no barcodes
    """
    cv2.setNumThreads(0)
    bar_manager = BarCodeManager()
    (_, _, box) = bar_manager.detect(thanks_obama)
    bar_manager.apply_barcode_blur(thanks_obama, box)
    cv2.setNumThreads(-1)