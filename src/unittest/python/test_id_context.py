"""
----------------------------------------------------------------------
Authors: Jan-Justin van Tonder
----------------------------------------------------------------------
Unit tests for the ID context module.
----------------------------------------------------------------------
"""

import pytest
from hutts_verification.id_contexts.sa_id_card import SAIDCard


def test_get_id_info_ignore_fields():
    """
    Test the case in which an ID number was found by get_id_info and whether it is used to extract other information
    such as date of birth, status and sex.
    """
    sa_id_card = SAIDCard()
    in_str = (
        'Identity Number\n'
        '7101135111011\n'
        'Surname\n'
        'Doe\n'
        'Names\n'
        'John-Michael\n'
        'Robert\n'
        'Nationality\n'
        'RSA\n'
        'Country of Birth\n'
        'RSA\n'
        'Status\n'
        'Citizen\n'
        'Sex\n'
        'M\n'
        'Date of Birth\n'
        '13 Jan 1971'
    )
    assert sa_id_card.get_id_info(in_str, ignore_fields=['nationality', 'status']) == {
        'identity_number': '7101135111011',
        'surname': 'Doe',
        'names': 'John-Michael Robert',
        'sex': 'M',
        'date_of_birth': '1971-01-13',
        'country_of_birth': 'RSA'
    }


def test_get_id_info_invalid_arg_in_str():
    """
    Test to see if get_id_info raises the correct exception when an incorrect type for the in_str arg is passed.
    """
    sa_id_card = SAIDCard()
    with pytest.raises(TypeError):
        sa_id_card.get_id_info(['not legit'])


def test_get_id_info_invalid_arg_barcode_data():
    """
    Test to see if get_id_info raises the correct exception when an incorrect type for the barcode_data arg is passed.
    """
    sa_id_card = SAIDCard()
    with pytest.raises(TypeError):
        sa_id_card.get_id_info('seems legit', barcode_data='nope')


def test_get_id_info_invalid_arg_ignore_fields():
    """
    Test to see if get_id_info raises the correct exception when an incorrect type for the ignore_fields arg is passed.
    """
    sa_id_card = SAIDCard()
    with pytest.raises(TypeError):
        sa_id_card.get_id_info('seems legit', ignore_fields='nah fam')


def test_get_id_info_invalid_arg_min_fuzzy_ratio():
    """
    Test to see if get_id_info raises the correct exception when an incorrect type for the min_fuzzy_ratio arg is passed.
    """
    sa_id_card = SAIDCard()
    with pytest.raises(TypeError):
        sa_id_card.get_id_info('good so far...', fuzzy_min_ratio='...fail')


def test_get_id_info_invalid_arg_max_multi_line():
    """
    Test to see if get_id_info raises the correct exception when an incorrect type for the max_multi_line arg is passed.
    """
    sa_id_card = SAIDCard()
    with pytest.raises(TypeError):
        sa_id_card.get_id_info('good so far...', max_multi_line=['...nevermind'])
