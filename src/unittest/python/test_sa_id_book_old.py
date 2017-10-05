"""
----------------------------------------------------------------------
Authors: Jan-Justin van Tonder
----------------------------------------------------------------------
Unit tests for the SA ID book old module.
----------------------------------------------------------------------
"""

import pytest
from id_contexts.sa_id_book_old import SAIDBookOld


def test_get_id_info_empty_in_str():
    """
    Test the case in which an empty string is passed to the get_id_info function.
    """
    sa_id_book = SAIDBookOld()
    assert sa_id_book.get_id_info('') == {
        'identity_number': None,
        'surname': None,
        'names': None,
        'sex': None,
        'date_of_birth': None,
        'country_of_birth': None,
        'status': None
    }


def test_get_id_info_default_skip_unnecessary():
    """
    Test the get_id_info function's ability to search for relevant (pre-specified) information.
    """
    sa_id_book = SAIDBookOld()
    in_str = (
        'Not legit\n'
        'SA Burger SA Citizen'
        'Ignore\n'
        'VanSurname\n'
        'Doe\n'
        'VoornameForenames\n'
        'John-Michael\n'
        'Robert\n'
        'Nationality\n'
        'RSA\n'
        'Geboortedistrik of-land\n'
        'District or Country of Birth\n'
        'SOUTH AFRICA\n'
        'Skip\n'
        'Skip this too\n'
        'Sex\n'
        'M\n'
        'geboortedatum 1971-01-13'
    )
    assert sa_id_book.get_id_info(in_str) == {
        'identity_number': None,
        'surname': 'Doe',
        'names': 'John-Michael Robert',
        'sex': 'M',
        'date_of_birth': '1971-01-13',
        'country_of_birth': 'South Africa',
        'status': 'Citizen',
    }


def test_get_id_info_default_id_num_found():
    """
    Test the case in which an ID number was found by get_id_info and whether it is used to extract other information
    such as date of birth, status and sex.
    """
    sa_id_book = SAIDBookOld()
    in_str = (
        'ID No 7101135111011\n'
        'VanSurname\n'
        'Doe\n'
        'VoornameForenames\n'
        'John-Michael\n'
        'Robert\n'
        'Geboortedistrik of-land\n'
        'District or Country of Birth\n'
        'South Africa\n'
        'geboortedatum 1971-01-13'
    )
    assert sa_id_book.get_id_info(in_str) == {
        'identity_number': '7101135111011',
        'surname': 'Doe',
        'names': 'John-Michael Robert',
        'sex': 'M',
        'date_of_birth': '1971-01-13',
        'country_of_birth': 'South Africa',
        'status': 'Citizen'
    }


def test_get_id_info_default_id_num_not_found():
    """
    Test the case in which an ID number was not found by get_id_info.
    """
    sa_id_book = SAIDBookOld()
    in_str = (
        'Nothing to find here... 7101135111011\n'
        'Not legit\n'
        'Ignore\n'
        'VanSurname\n'
        'Doe\n'
        'VoornameForenames\n'
        'John-Michael\n'
        'Robert\n'
        'Nationality\n'
        'RSA\n'
        'Geboortedistrik of-land\n'
        'District or Country of Birth\n'
        'South Africa\n'
        'Skip\n'
        'Skip this too\n'
        'Status\n'
        'Hungry\n'
        'Sex\n'
        'M\n'
        'geboortedatum 1971-01-13'
    )
    assert sa_id_book.get_id_info(in_str) == {
        'identity_number': None,
        'surname': 'Doe',
        'names': 'John-Michael Robert',
        'sex': 'M',
        'date_of_birth': '1971-01-13',
        'country_of_birth': 'South Africa',
        'status': None
    }


def test_get_id_info_id_in_barcode():
    """
    Test the case in which an ID number was extracted from a barcode and passed to get_id_info and whether it is used to
    extract other information such as date of birth, status and sex.
    """
    sa_id_book = SAIDBookOld()
    in_str = (
        'id no 123456789\n'
        'VanSurname\n'
        'Doe\n'
        'VoornameForenames\n'
        'Jane-Michael\n'
        'Robert'
    )
    assert sa_id_book.get_id_info(in_str, barcode_data={'identity_number': '7101134111111'}) == {
        'identity_number': '7101134111111',
        'surname': 'Doe',
        'names': 'Jane-Michael Robert',
        'sex': 'F',
        'date_of_birth': '1971-01-13',
        'country_of_birth': None,
        'status': 'Non Citizen'
    }


def test_get_id_info_multi_line_1():
    """
    Test the ability of the get_id_info function to retrieve field values over multiple lines.
    This case checks for a maximum of 2 lines.
    """
    sa_id_book = SAIDBookOld()
    in_str = (
        'id no 7101135111011\n'
        'VanSurname\n'
        'Doe\n'
        'VoornameForenames\n'
        'John-Michael\n'
        'Robert\n'
        'Ignore'
    )
    assert sa_id_book.get_id_info(in_str) == {
        'identity_number': '7101135111011',
        'surname': 'Doe',
        'names': 'John-Michael Robert',
        'sex': 'M',
        'date_of_birth': '1971-01-13',
        'country_of_birth': None,
        'status': 'Citizen'
    }


def test_get_id_info_multi_line_2():
    """
    Test the ability of the get_id_info function to retrieve field values over multiple lines.
    This case checks if a match to multi_line_end was found.
    """
    sa_id_book = SAIDBookOld()
    in_str = (
        'id no 7101135111011\n'
        'VanSurname\n'
        'Doe\n'
        'VoornameForenames\n'
        'John-Michael'
    )
    assert sa_id_book.get_id_info(in_str) == {
        'identity_number': '7101135111011',
        'surname': 'Doe',
        'names': 'John-Michael',
        'sex': 'M',
        'date_of_birth': '1971-01-13',
        'country_of_birth': None,
        'status': 'Citizen'
    }


def test_get_id_info_multi_line_3():
    """
    Test the ability of the get_id_info function to retrieve field values over multiple lines.
    This case checks how a specified multi_line field value is dealt with if the value does not exist at the end of
    the in_string.
    """
    sa_id_book = SAIDBookOld()
    in_str = 'Forenames'
    assert sa_id_book.get_id_info(in_str) == {
        'identity_number': None,
        'surname': None,
        'names': None,
        'sex': None,
        'date_of_birth': None,
        'country_of_birth': None,
        'status': None
    }


def test_get_id_info_bare_multi_line_4():
    """
    Test the ability of the get_id_info function to retrieve field values over multiple lines.
    This case checks how a specified multi_line field value is dealt with if the value exists, but is at the end of
    the in_string.
    """
    sa_id_book = SAIDBookOld()
    in_str = (
        'VanSurname\n'
        'Doe\n'
        'VoornameForenames\n'
        'John\n'
        'Robert'
    )
    assert sa_id_book.get_id_info(in_str, max_multi_line=4) == {
        'identity_number': None,
        'surname': 'Doe',
        'names': 'John Robert',
        'sex': None,
        'date_of_birth': None,
        'country_of_birth': None,
        'status': None
    }


def test_get_id_info_max_multi_line():
    """
    Test the ability of the get_id_info function to retrieve field values over multiple lines.
    This case checks if the correct number of multi_line was considered when specified.
    """
    sa_id_book = SAIDBookOld()
    in_str = (
        'ID NO 7101135111011\n'
        'VanSurname\n'
        'Doe\n'
        'VoornameForenames\n'
        'John-Michael\n'
        'Robert\n'
        'Douglas\n'
        'Ignore'
    )
    assert sa_id_book.get_id_info(in_str, max_multi_line=3) == {
        'identity_number': '7101135111011',
        'surname': 'Doe',
        'names': 'John-Michael Robert Douglas',
        'sex': 'M',
        'date_of_birth': '1971-01-13',
        'country_of_birth': None,
        'status': 'Citizen'
    }


def test_get_id_info_fuzzy_1():
    """
    Tests to see if get_id_info is capable of retrieving field values through reasonable or commonly required fuzzy
    matching to be performed.
    """
    sa_id_book = SAIDBookOld()
    in_str = (
        'Ide nom 7101135111011\n'
        'VanSuriname\n'
        'Doe\n'
        'VoornameForenames\n'
        'John-Michael\n'
        'Robert\n'
        'Gebooortedistrikt or-sand\n'
        'Distric r County o Bnth\n'
        'SUID-AFRIKA\n'
    )
    assert sa_id_book.get_id_info(in_str) == {
        'identity_number': '7101135111011',
        'surname': 'Doe',
        'names': 'John-Michael Robert',
        'sex': 'M',
        'date_of_birth': '1971-01-13',
        'country_of_birth': 'South Africa',
        'status': 'Citizen'
    }


def test_get_id_info_fuzzy_2():
    """
    Tests to see if get_id_info is capable of retrieving field values through reasonable or commonly required fuzzy
    matching to be performed.
    """
    sa_id_book = SAIDBookOld()
    in_str = (
        'ed no 7101135111011\n'
        'VanSuriname 00ee\n'
        'Doe\n'
        'vornamef0renames iii\n'
        'John-Michael\n'
        'Robert\n'
        'Geb00rtedistrikt 0r-sand\n'
        'dstrct or country 0 bnth\n'
        'SUID-AFRIKA\n'
    )
    assert sa_id_book.get_id_info(in_str) == {
        'identity_number': '7101135111011',
        'surname': 'Doe',
        'names': 'John-Michael Robert',
        'sex': 'M',
        'date_of_birth': '1971-01-13',
        'country_of_birth': 'South Africa',
        'status': 'Citizen'
    }


def test_get_id_info_fuzzy_min_ratio():
    """
    Tests the get_id_info function fuzzy matching with a specified minimum ratio.
    """
    sa_id_book = SAIDBookOld()
    in_str = (
        'edn0 7101135111011\n'
        'VanSuriname\n'
        'Doe\n'
        'VoornameForenames\n'
        'John-Michael\n'
        'Robert\n'
        'Sex\n'
        'M\n'
        'Geb00rtedistrikt 0r-sand\n'
        'dstrct or county 0 bnth\n'
        'South Africa\n'
    )
    assert sa_id_book.get_id_info(in_str, fuzzy_min_ratio=90.00) == {
        'identity_number': None,
        'surname': 'Doe',
        'names': 'John-Michael Robert',
        'sex': 'M',
        'date_of_birth': None,
        'country_of_birth': None,
        'status': None
    }


def test_get_id_info_bare():
    """
    Test the get_id_info function's behaviour when a field name is matched, but no field value follows and is at the end
    of the in_string.
    """
    sa_id_book = SAIDBookOld()
    in_str = (
        'VanSurname\n'
    )
    assert sa_id_book.get_id_info(in_str) == {
        'identity_number': None,
        'surname': None,
        'names': None,
        'sex': None,
        'date_of_birth': None,
        'country_of_birth': None,
        'status': None
    }


def test_get_id_info_invalid_date_of_birth():
    """
    Test the get_id_info function's behaviour when an invalid date of birth is given for formatting.
    We expect it return the malformed 'date'.
    """
    sa_id_book = SAIDBookOld()
    in_str = (
        'geboortedatum 123-0-1971\n'
        'Geboortedistrik of-land\n'
        'District or Country of Birth\n'
        'South Africa'
    )
    assert sa_id_book.get_id_info(in_str) == {
        'identity_number': None,
        'surname': None,
        'names': None,
        'sex': None,
        'date_of_birth': '123-0-1971',
        'country_of_birth': 'South Africa',
        'status': None
    }
