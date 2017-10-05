"""
----------------------------------------------------------------------
Authors: Jan-Justin van Tonder
----------------------------------------------------------------------
Unit tests for the SA ID module.
----------------------------------------------------------------------
"""

import pytest
from id_contexts.sa_id_card import SAIDCard


def test_validate_id_number_valid():
    """
    Tests to see if the validate_id_number function correctly validates the given id number.
    This case tests whether it deems a valid id number as valid.
    """
    sa_id = SAIDCard()
    assert sa_id.validate_id_number('7209170838080')


def test_validate_id_number_invalid():
    """
    Tests to see if the validate_id_number function correctly validates the given id number.
    This case tests whether it deems a invalid id number as invalid.
    """
    sa_id = SAIDCard()
    assert not sa_id.validate_id_number('1234567891011')


def test_validate_id_number_valid_length_specified():
    """
    Tests to see if the validate_id_number function correctly validates the given id number.
    This case tests the behaviour of specifying the valid_length arg
    """
    sa_id = SAIDCard()
    assert not sa_id.validate_id_number('1234567891011', valid_length=15)


def test_validate_id_number_invalid_arg_id_number_1():
    """
    Tests to see if the validate_id_number function raises the correct exception for an invalid id_number arg.
    """
    sa_id = SAIDCard()
    with pytest.raises(TypeError):
        sa_id.validate_id_number(123456)


def test_validate_id_number_invalid_arg_id_number_2():
    """
    Tests to see if the validate_id_number function raises the correct exception for an invalid id_number arg.
    """
    sa_id = SAIDCard()
    with pytest.raises(TypeError):
        sa_id.validate_id_number('1234Almost56')


def test_validate_id_number_invalid_arg_valid_length():
    """
    Tests to see if the validate_id_number function raises the correct exception for an invalid valid_length arg.
    """
    sa_id = SAIDCard()
    with pytest.raises(TypeError):
        sa_id.validate_id_number('1234567891011', False)
