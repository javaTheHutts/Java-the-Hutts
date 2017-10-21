"""
----------------------------------------------------------------------
Authors: Jan-Justin van Tonder
----------------------------------------------------------------------
Unit tests for the SA ID card module.
----------------------------------------------------------------------
"""

from id_contexts.sa_id_card import SAIDCard


def test_get_id_info_empty_in_str():
    """
    Test the case in which an empty string is passed to the get_id_info function.
    """
    sa_id_card = SAIDCard()
    assert sa_id_card.get_id_info('') == {
        'identity_number': None,
        'surname': None,
        'names': None,
        'sex': None,
        'date_of_birth': None,
        'country_of_birth': None,
        'status': None,
        'nationality': None
    }


def test_get_id_info_default_skip_unnecessary():
    """
    Test the get_id_info function's ability to search for relevant (pre-specified) information.
    """
    sa_id_card = SAIDCard()
    in_str = (
        'Not legit\n'
        'Ignore\n'
        'Surname\n'
        'Doe\n'
        'Names\n'
        'John-Michael\n'
        'Robert\n'
        'Nationality\n'
        'RSA\n'
        'Country of Birth\n'
        'RSA\n'
        'Skip\n'
        'Skip this too\n'
        'Status\n'
        'Citizen\n'
        'Sex\n'
        'M\n'
        'Date of Birth\n'
        '13 Jan 1971'
    )
    assert sa_id_card.get_id_info(in_str) == {
        'identity_number': None,
        'surname': 'Doe',
        'names': 'John-Michael Robert',
        'sex': 'M',
        'date_of_birth': '1971-01-13',
        'country_of_birth': 'RSA',
        'status': 'Citizen',
        'nationality': 'RSA'
    }


def test_get_id_info_default_id_num_found():
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
    assert sa_id_card.get_id_info(in_str) == {
        'identity_number': '7101135111011',
        'surname': 'Doe',
        'names': 'John-Michael Robert',
        'sex': 'M',
        'date_of_birth': '1971-01-13',
        'country_of_birth': 'RSA',
        'status': 'Citizen',
        'nationality': 'RSA'
    }


def test_get_id_info_default_id_num_not_found():
    """
    Test the case in which an ID number was not found by get_id_info.
    """
    sa_id_card = SAIDCard()
    in_str = (
        'Nothing to find here...\n'
        '7101135111011\n'
        'Not legit\n'
        'Ignore\n'
        'Surname\n'
        'Doe\n'
        'Names\n'
        'John-Michael\n'
        'Robert\n'
        'Nationality\n'
        'RSA\n'
        'Country of Birth\n'
        'RSA\n'
        'Skip\n'
        'Skip this too\n'
        'Status\n'
        'Hungry\n'
        'Sex\n'
        'M\n'
        'Date of Birth\n'
        '13 Jan 1971'
    )
    assert sa_id_card.get_id_info(in_str) == {
        'identity_number': None,
        'surname': 'Doe',
        'names': 'John-Michael Robert',
        'sex': 'M',
        'date_of_birth': '1971-01-13',
        'country_of_birth': 'RSA',
        'status': 'Hungry',
        'nationality': 'RSA'
    }


def test_get_id_info_id_in_barcode():
    """
    Test the case in which an ID number was extracted from a barcode and passed to get_id_info and whether it is used
    to extract other information such as date of birth, status and sex.
    """
    sa_id_card = SAIDCard()
    in_str = (
        'Identity Number\n'
        '123456789\n'
        'Surname\n'
        'Doe\n'
        'Names\n'
        'Jane-Michael\n'
        'Robert'
    )
    assert sa_id_card.get_id_info(in_str, barcode_data={'identity_number': '7101134111111'}) == {
        'identity_number': '7101134111111',
        'surname': 'Doe',
        'names': 'Jane-Michael Robert',
        'sex': 'F',
        'date_of_birth': '1971-01-13',
        'country_of_birth': None,
        'status': 'Non Citizen',
        'nationality': None
    }


def test_get_id_info_multi_line_1():
    """
    Test the ability of the get_id_info function to retrieve field values over multiple lines.
    This case checks for a maximum of 2 lines.
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
        'Ignore'
        'Sex\n'
        'M'
    )
    assert sa_id_card.get_id_info(in_str) == {
        'identity_number': '7101135111011',
        'surname': 'Doe',
        'names': 'John-Michael Robert',
        'sex': 'M',
        'date_of_birth': '1971-01-13',
        'country_of_birth': None,
        'status': 'Citizen',
        'nationality': None
    }


def test_get_id_info_multi_line_2():
    """
    Test the ability of the get_id_info function to retrieve field values over multiple lines.
    This case checks if a match to multi_line_end was found.
    """
    sa_id_card = SAIDCard()
    in_str = (
        'Identity Number\n'
        '7101135111011\n'
        'Surname\n'
        'Doe\n'
        'Names\n'
        'John-Michael\n'
        'Sex\n'
        'M'
    )
    assert sa_id_card.get_id_info(in_str) == {
        'identity_number': '7101135111011',
        'surname': 'Doe',
        'names': 'John-Michael',
        'sex': 'M',
        'date_of_birth': '1971-01-13',
        'country_of_birth': None,
        'status': 'Citizen',
        'nationality': None
    }


def test_get_id_info_multi_line_3():
    """
    Test the ability of the get_id_info function to retrieve field values over multiple lines.
    This case checks how a specified multi_line field value is dealt with if the value does not exist at the end of
    the in_string.
    """
    sa_id_card = SAIDCard()
    in_str = (
        'Names'
    )
    assert sa_id_card.get_id_info(in_str) == {
        'identity_number': None,
        'surname': None,
        'names': None,
        'sex': None,
        'date_of_birth': None,
        'country_of_birth': None,
        'status': None,
        'nationality': None
    }


def test_get_id_info_bare_multi_line_4():
    """
    Test the ability of the get_id_info function to retrieve field values over multiple lines.
    This case checks how a specified multi_line field value is dealt with if the value exists, but is at the end of
    the in_string.
    """
    sa_id_card = SAIDCard()
    in_str = (
        'Surname\n'
        'Doe\n'
        'Names\n'
        'John\n'
        'Robert'
    )
    assert sa_id_card.get_id_info(in_str, max_multi_line=4) == {
        'identity_number': None,
        'surname': 'Doe',
        'names': 'John Robert',
        'sex': None,
        'date_of_birth': None,
        'country_of_birth': None,
        'status': None,
        'nationality': None
    }


def test_get_id_info_max_multi_line():
    """
    Test the ability of the get_id_info function to retrieve field values over multiple lines.
    This case checks if the correct number of multi_line was considered when specified.
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
        'Douglas\n'
        'Ignore'
        'Sex\n'
        'M'
    )
    assert sa_id_card.get_id_info(in_str, max_multi_line=3) == {
        'identity_number': '7101135111011',
        'surname': 'Doe',
        'names': 'John-Michael Robert Douglas',
        'sex': 'M',
        'date_of_birth': '1971-01-13',
        'country_of_birth': None,
        'status': 'Citizen',
        'nationality': None
    }


def test_get_id_info_fuzzy_1():
    """
    Tests to see if get_id_info is capable of retrieving field values through reasonable or commonly required fuzzy
    matching to be performed.
    """
    sa_id_card = SAIDCard()
    in_str = (
        'Idenmy Number\n'
        '7101135111011\n'
        'Suriname\n'
        'Doe\n'
        'Names\n'
        'John-Michael\n'
        'Robert\n'
        'Sex\n'
        'M\n'
        'Nahonallly\n'
        'RSA\n'
    )
    assert sa_id_card.get_id_info(in_str) == {
        'identity_number': '7101135111011',
        'surname': 'Doe',
        'names': 'John-Michael Robert',
        'sex': 'M',
        'date_of_birth': '1971-01-13',
        'country_of_birth': None,
        'status': 'Citizen',
        'nationality': 'RSA'
    }


def test_get_id_info_fuzzy_2():
    """
    Tests to see if get_id_info is capable of retrieving field values through reasonable or commonly required fuzzy
    matching to be performed.
    """
    sa_id_card = SAIDCard()
    in_str = (
        'Idenmy Number lll\n'
        '7101135111011\n'
        'Suriname 00ee\n'
        'Doe\n'
        'Names iii\n'
        'John-Michael\n'
        'Robert\n'
        'Seeex\n'
        'M\n'
        'Nahonallly\n'
        'RSA\n'
    )
    assert sa_id_card.get_id_info(in_str) == {
        'identity_number': '7101135111011',
        'surname': 'Doe',
        'names': 'John-Michael Robert',
        'sex': 'M',
        'date_of_birth': '1971-01-13',
        'country_of_birth': None,
        'status': 'Citizen',
        'nationality': 'RSA'
    }


def test_get_id_info_fuzzy_min_ratio():
    """
    Tests the get_id_info function fuzzy matching with a specified minimum ratio.
    """
    sa_id_card = SAIDCard()
    in_str = (
        'Idenmy Number lll\n'
        '7101135111011\n'
        'Suriname\n'
        'Doe\n'
        'Names\n'
        'John-Michael\n'
        'Robert\n'
        'Sex\n'
        'M\n'
        'Nahonallly\n'
        'RSA\n'
    )
    assert sa_id_card.get_id_info(in_str, fuzzy_min_ratio=90.00) == {
        'identity_number': None,
        'surname': 'Doe',
        'names': 'John-Michael Robert',
        'sex': 'M',
        'date_of_birth': None,
        'country_of_birth': None,
        'status': None,
        'nationality': None
    }


def test_get_id_info_bare():
    """
    Test the get_id_info function's behaviour when a field name is matched, but no field value follows and is at the end
    of the in_string.
    """
    sa_id_card = SAIDCard()
    in_str = (
        'Surname\n'
    )
    assert sa_id_card.get_id_info(in_str) == {
        'identity_number': None,
        'surname': None,
        'names': None,
        'sex': None,
        'date_of_birth': None,
        'country_of_birth': None,
        'status': None,
        'nationality': None
    }


def test_get_id_info_invalid_date_of_birth():
    """
    Test the get_id_info function's behaviour when an invalid date of birth is given for formatting.
    We expect it return the malformed 'date'.
    """
    sa_id_card = SAIDCard()
    in_str = (
        'date of birth\n'
        '123 Jin 1971\n'
        'country of birth\n'
        'RSA'
    )
    assert sa_id_card.get_id_info(in_str) == {
        'identity_number': None,
        'surname': None,
        'names': None,
        'sex': None,
        'date_of_birth': '123 Jin 1971',
        'country_of_birth': 'RSA',
        'status': None,
        'nationality': None
    }
