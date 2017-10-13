"""
----------------------------------------------------------------------
Authors: Jan-Justin van Tonder
----------------------------------------------------------------------
Unit tests for the Verify Text module.
----------------------------------------------------------------------
"""

import pytest
from hutts_verification.verification.text_verify import TextVerify


def test_verify_blank():
    """
    Tests the verify function with blank args.
    """
    verifier = TextVerify()
    assert verifier.verify({}, {}) == (False, 0.0)


def test_verify_default():
    """
    Tests the return value of the verify function with default args.
    """
    verifier = TextVerify()
    extracted_info = {
        'identity_number': '7101135111011',
        'surname': 'Doe',
        'names': 'John-Michael Robert',
        'sex': '####################################',
        'date_of_birth': '71-01-13',
        'country_of_birth': 'RSA',
        'status': 'Citizen',
        'nationality': 'RSA'
    }
    verifier_info = {
        'identity_number': '7101135111011',
        'surname': 'Doe',
        'names': 'John-Michael Robert',
        'sex': 'M',
        'date_of_birth': '71-01-13',
        'country_of_birth': 'RSA',
        'status': 'Citizen',
        'nationality': 'RSA'
    }
    assert verifier.verify(extracted_info, verifier_info) == (True, 87.5)


def test_verify_default_no_match():
    """
    Tests the return value of the verify function with default args.
    In this case we expect a 0% match.
    """
    verifier = TextVerify()
    extracted_info = {
        'identity_number': '####################################',
        'surname': '####################################',
        'names': '####################################',
        'sex': '####################################',
        'date_of_birth': '####################################',
        'country_of_birth': '####################################',
        'status': '####################################',
        'nationality': '####################################'
    }
    verifier_info = {
        'identity_number': '7101135111011',
        'surname': 'Doe',
        'names': 'John-Michael Robert',
        'sex': 'M',
        'date_of_birth': '71-01-13',
        'country_of_birth': 'RSA',
        'status': 'Citizen',
        'nationality': 'RSA'
    }
    assert verifier.verify(extracted_info, verifier_info) == (False, 0.0)


def test_verify_default_half_match():
    """
    Tests the return value of the verify function with default args.
    In this case we expect a 50% match.
    """
    verifier = TextVerify()
    extracted_info = {
        'identity_number': '7101135111011',
        'surname': 'Doe',
        'names': 'John-Michael Robert',
        'sex': 'M',
        'date_of_birth': '####################################',
        'country_of_birth': '####################################',
        'status': '####################################',
        'nationality': '####################################'
    }
    verifier_info = {
        'identity_number': '7101135111011',
        'surname': 'Doe',
        'names': 'John-Michael Robert',
        'sex': 'M',
        'date_of_birth': '71-01-13',
        'country_of_birth': 'RSA',
        'status': 'Citizen',
        'nationality': 'RSA'
    }
    assert verifier.verify(extracted_info, verifier_info) == (False, 50.0)


def test_verify_default_full_match():
    """
    Tests the return value of the verify function with default args.
    In this case we expect a 100% match.
    """
    verifier = TextVerify()
    extracted_info = {
        'identity_number': '7101135111011',
        'surname': 'Doe',
        'names': 'John-Michael Robert',
        'sex': 'M',
        'date_of_birth': '71-01-13',
        'country_of_birth': 'RSA',
        'status': 'Citizen',
        'nationality': 'RSA'
    }
    verifier_info = {
        'identity_number': '7101135111011',
        'surname': 'Doe',
        'names': 'John-Michael Robert',
        'sex': 'M',
        'date_of_birth': '71-01-13',
        'country_of_birth': 'RSA',
        'status': 'Citizen',
        'nationality': 'RSA'
    }
    assert verifier.verify(extracted_info, verifier_info) == (True, 100.0)


def test_verify_threshold():
    """
    Tests the return value of the verify function with a specified threshold arg.
    """
    verifier = TextVerify()
    extracted_info = {
        'identity_number': '7101135111011',
        'surname': 'Doe',
        'names': 'John-Michael Robert',
        'sex': '####################################',
        'date_of_birth': '71-01-13',
        'country_of_birth': 'RSA',
        'status': 'Citizen',
        'nationality': 'RSA'
    }
    verifier_info = {
        'identity_number': '7101135111011',
        'surname': 'Doe',
        'names': 'John-Michael Robert',
        'sex': 'M',
        'date_of_birth': '71-01-13',
        'country_of_birth': 'RSA',
        'status': 'Citizen',
        'nationality': 'RSA'
    }
    assert verifier.verify(extracted_info, verifier_info, threshold=90.0) == (False, 87.5)


def test_verify_min_matches():
    """
    Tests the return value of the verify function with a specified minimum number of matches arg.
    """
    verifier = TextVerify()
    extracted_info = {
        'identity_number': '7101135111011',
        'surname': 'Doe',
        'names': 'John-Michael Robert',
        'sex': 'M',
        'not valid': '####################################',
        'not legit': '####################################',
        'not gonna work': '####################################',
        'try again': '####################################'
    }
    verifier_info = {
        'identity_number': '7101135111011',
        'surname': 'Doe',
        'names': 'John-Michael Robert',
        'sex': 'M',
        'date_of_birth': '71-01-13',
        'country_of_birth': 'RSA',
        'status': 'Citizen',
        'nationality': 'RSA'
    }
    assert verifier.verify(extracted_info, verifier_info, min_matches=6) == (False, 0.0)


def test_verify_verbose_1():
    """
    Tests the return value of the verify function with a specified verbose arg.
    """
    verifier = TextVerify()
    extracted_info = {
        'identity_number': '7101135111011',
        'surname': 'Door',
        'names': 'John-Michael Robert',
        'sex': 'M',
        'date_of_birth': '71-01-13',
        'country_of_birth': 'GRSAGT',
        'status': 'Cytyziny',
        'nationality': 'RSA'
    }
    verifier_info = {
        'identity_number': '7101135111011',
        'surname': 'Doe',
        'names': 'John-Michael Robert',
        'sex': 'M',
        'date_of_birth': '71-01-13',
        'country_of_birth': 'RSA',
        'status': 'Citizen',
        'nationality': 'RSA'
    }
    assert verifier.verify(extracted_info, verifier_info, verbose=True) == (True, {
        'identity_number': {
            'match_percentage': 100.0,
            'verifier_field_value': '7101135111011',
            'extracted_field_value': '7101135111011'
        },
        'surname': {
            'match_percentage': 57.14,
            'verifier_field_value': 'Doe',
            'extracted_field_value': 'Door'
        },
        'names': {
            'match_percentage': 100.0,
            'verifier_field_value': 'John-Michael Robert',
            'extracted_field_value': 'John-Michael Robert'
        },
        'sex': {
            'match_percentage': 100.0,
            'verifier_field_value': 'M',
            'extracted_field_value': 'M'
        },
        'date_of_birth': {
            'match_percentage': 100.0,
            'verifier_field_value': '71-01-13',
            'extracted_field_value': '71-01-13'
        },
        'country_of_birth': {
            'match_percentage': 66.67,
            'verifier_field_value': 'RSA',
            'extracted_field_value': 'GRSAGT'
        },
        'status': {
            'match_percentage': 53.33,
            'verifier_field_value': 'Citizen',
            'extracted_field_value': 'Cytyziny'
        },
        'nationality': {
            'match_percentage': 100.0,
            'verifier_field_value': 'RSA',
            'extracted_field_value': 'RSA'
        },
        'total': 84.64
    })


def test_verify_verbose_2():
    """
    Tests the return value of the verify function with a specified verbose arg.
    """
    verifier = TextVerify()
    extracted_info = {
        'identity_number': '7101135111011',
        'surname': 'Door',
        'names': 'John-Michael Robert',
        'sex': 'M',
        'date_of_birth': '71-01-13',
        'country_of_birth': 'GRSAGT',
        'nationality': 'RSA'
    }
    verifier_info = {
        'identity_number': '7101135111011',
        'surname': 'Doe',
        'names': 'John-Michael Robert',
        'sex': 'M',
        'date_of_birth': '71-01-13',
        'country_of_birth': 'RSA',
        'status': 'Citizen',
    }
    assert verifier.verify(extracted_info, verifier_info, verbose=True) == (True, {
        'identity_number': {
            'match_percentage': 100.0,
            'verifier_field_value': '7101135111011',
            'extracted_field_value': '7101135111011'
        },
        'surname': {
            'match_percentage': 57.14,
            'verifier_field_value': 'Doe',
            'extracted_field_value': 'Door'
        },
        'names': {
            'match_percentage': 100.0,
            'verifier_field_value': 'John-Michael Robert',
            'extracted_field_value': 'John-Michael Robert'
        },
        'sex': {
            'match_percentage': 100.0,
            'verifier_field_value': 'M',
            'extracted_field_value': 'M'
        },
        'date_of_birth': {
            'match_percentage': 100.0,
            'verifier_field_value': '71-01-13',
            'extracted_field_value': '71-01-13'
        },
        'country_of_birth': {
            'match_percentage': 66.67,
            'verifier_field_value': 'RSA',
            'extracted_field_value': 'GRSAGT'
        },
        'status': {
            'match_percentage': None,
            'verifier_field_value': 'Citizen',
            'extracted_field_value': None
        },
        'nationality': {
            'match_percentage': None,
            'verifier_field_value': None,
            'extracted_field_value': 'RSA'
        },
        'total': 87.3
    })


def test_verify_invalid_arg_extracted_1():
    """
    Tests to see if the verify function raises the correct exception for an invalid extracted arg.
    """
    verifier = TextVerify()
    with pytest.raises(TypeError):
        verifier.verify('not quite', {})


def test_verify_invalid_arg_extracted_2():
    """
    Tests to see if the verify function raises the correct exception for an invalid extracted arg.
    """
    verifier = TextVerify()
    with pytest.raises(TypeError):
        verifier.verify({'identity_number': 1234}, {'identity_number': '7101135111011'})


def test_verify_invalid_arg_verifier_1():
    """
    Tests to see if the verify function raises the correct exception for an invalid verifier arg.
    """
    verifier = TextVerify()
    with pytest.raises(TypeError):
        verifier.verify({}, 'does not seem legit')


def test_verify_invalid_arg_verifier_2():
    """
    Tests to see if the verify function raises the correct exception for an invalid verifier arg.
    """
    verifier = TextVerify()
    with pytest.raises(TypeError):
        verifier.verify({'names': 'John Legit'}, {'names': ['not', 'John', 'legit']})


def test_verify_invalid_arg_threshold():
    """
    Tests to see if the verify function raises the correct exception for an invalid threshold arg.
    """
    verifier = TextVerify()
    with pytest.raises(TypeError):
        verifier.verify({}, {}, threshold=['nope'])


def test_verify_invalid_arg_min_matches():
    """
    Tests to see if the verify function raises the correct exception for an invalid min_matches arg.
    """
    verifier = TextVerify()
    with pytest.raises(TypeError):
        verifier.verify({}, {}, min_matches=['nope again'])


def test_verify_invalid_arg_verbose():
    """
    Tests to see if the verify function raises the correct exception for an invalid verbose arg.
    """
    verifier = TextVerify()
    with pytest.raises(TypeError):
        verifier.verify({}, {}, verbose='nah fam')
