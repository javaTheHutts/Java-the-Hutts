"""
----------------------------------------------------------------------
Authors: Marno Hermann
----------------------------------------------------------------------
Unit tests for the Template Matching
----------------------------------------------------------------------
"""
import pytest
import cv2
import os
from hutts_verification.image_preprocessing.template_matching import TemplateMatching

TEMPLATE_DIR = "{base_path}/../../main/python/hutts_verification/image_preprocessing/templates/".format(
    base_path=os.path.abspath(os.path.dirname(__file__)))
student_card = cv2.imread(TEMPLATE_DIR + "pp2.jpg")
id_book = cv2.imread(TEMPLATE_DIR + "temp_flag.jpg")
brick = cv2.imread(TEMPLATE_DIR + "bricks.png")

dimension_ratio = 900.0 / brick.shape[1]
dim = (900, int(brick.shape[0] * dimension_ratio))
no_match = cv2.resize(brick, dim, interpolation=cv2.INTER_AREA)

dim = (1000, 200)
wrong_dim = cv2.resize(brick, dim, interpolation=cv2.INTER_AREA)

direct_match = cv2.imread(TEMPLATE_DIR + "ID.jpg")


def test_wrong_param():
    template = TemplateMatching()
    with pytest.raises(TypeError):
        assert template.identify(21)


def test_match_template():
    template = TemplateMatching()
    cv2.setNumThreads(0)
    assert template.identify(direct_match) is 'idcard'
    cv2.setNumThreads(-1)


def test_wrong_dim_template():
    template = TemplateMatching()
    cv2.setNumThreads(0)
    assert template.identify(wrong_dim) is 'None'
    cv2.setNumThreads(-1)


def test_no_match_template():
    template = TemplateMatching()
    cv2.setNumThreads(0)
    assert template.identify(no_match) is 'None'
    cv2.setNumThreads(-1)


def test_student_template():
    template = TemplateMatching()
    cv2.setNumThreads(0)
    assert template.identify(student_card) is 'studentcard'
    cv2.setNumThreads(-1)


def test_to_small_template():
    template = TemplateMatching()
    cv2.setNumThreads(0)
    assert template.identify(id_book) is 'None'
    cv2.setNumThreads(-1)
