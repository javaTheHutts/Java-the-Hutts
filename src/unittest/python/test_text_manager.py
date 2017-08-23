"""
----------------------------------------------------------------------
Authors: Jan-Justin van Tonder
----------------------------------------------------------------------
Unit tests for the Text Manager module.
----------------------------------------------------------------------
"""

import pytest
from image_processing.text_manager import TextManager


def test_clean_up_empty_in_str():
    """
    Test the case in which an empty string is passed to the cleanup function.
    """
    txt_man = TextManager()
    assert txt_man.clean_up('') == ''


def test_clean_up_unicode_support():
    """
    Test support for unicode characters in the cleanup function.
    """
    txt_man = TextManager()
    in_str = (
        'Identity Number\n'
        '123456789\n'
        'Surname\n'
        'Döe\n'
        'Names\n'
        'John-Micháel\n'
        'Robert'
    )
    assert txt_man.clean_up(in_str) == (
        'Identity Number\n'
        '123456789\n'
        'Surname\n'
        'Döe\n'
        'Names\n'
        'John-Micháel\n'
        'Robert'
    )


def test_clean_up_remove_multiple_newlines():
    """
    Test the removal of multiple newlines in the clean up function.
    """
    txt_man = TextManager()
    in_str = (
        'Identity Number\n\n\n'
        '123456789\n'
        'Surname\n'
        'Doe\n\n'
        'Names\n\n'
        'John-Michael\n'
        'Robert\n'
    )
    assert txt_man.clean_up(in_str) == (
        'Identity Number\n'
        '123456789\n'
        'Surname\n'
        'Doe\n'
        'Names\n'
        'John-Michael\n'
        'Robert'
    )


def test_clean_up_remove_multiple_spaces():
    """
    Test the removal of multiple spaces in the clean up function.
    """
    txt_man = TextManager()
    in_str = (
        'Identity Number\n'
        '123456789\n'
        'Surname\n'
        'Doe\n'
        'Names\n'
        'John     Michael   Robert'
    )
    assert txt_man.clean_up(in_str) == (
        'Identity Number\n'
        '123456789\n'
        'Surname\n'
        'Doe\n'
        'Names\n'
        'John Michael Robert'
    )


def test_clean_up_remove_default():
    """
    Test the default clean up function's removal.
    """
    txt_man = TextManager()
    in_str = (
        'Identity #Number\n'
        '123456789...\n'
        '$Sur_name&\n'
        '\\/Doe.\n'
        'Names*\n'
        'John-Michae|l\n'
        'R%obert+'
    )
    assert txt_man.clean_up(in_str) == (
        'Identity Number\n'
        '123456789\n'
        'Surname\n'
        'Doe\n'
        'Names\n'
        'John-Michael\n'
        'Robert'
    )


def test_clean_up_remove_specified():
    """
    Test the clean up function's removal with an additional list of characters to remove.
    """
    txt_man = TextManager()
    in_str = (
        'Identity Number\n'
        '123456789\n'
        'Surname\n'
        'Döe\n'
        'Names\n'
        'John+Michael\n'
        'Robert'
    )
    assert txt_man.clean_up(in_str, ['+', 'ö']) == (
        'Identity Number\n'
        '123456789\n'
        'Surname\n'
        'De\n'
        'Names\n'
        'JohnMichael\n'
        'Robert'
    )


def test_clean_up_remove_specified_overwrite():
    """
    Test the clean up function's removal with a specified list of characters that overwrites the default list.
    """
    txt_man = TextManager()
    in_str = (
        'Identity Number\n'
        '123456789\n'
        'Surname\n'
        'Döe_\n'
        'Names\n'
        'John-Michael\n'
        'Robert'
    )
    assert txt_man.clean_up(in_str, ['ö', '-'], False) == (
        'Identity Number\n'
        '123456789\n'
        'Surname\n'
        'De_\n'
        'Names\n'
        'JohnMichael\n'
        'Robert'
    )


def test_clean_up_remove_specified_sanitise():
    """
    Test the clean up function's removal with an additional list of characters to remove, but tests to see if certain
    control characters used within the underlying regex, such as ], [, ^ and -, are escaped.
    """
    txt_man = TextManager()
    in_str = (
        'Identity Number\n'
        '123456789\n'
        'Surname\n'
        'Doe[^-]\n'
        'Names\n'
        'John-Michael\n'
        'Robert'
    )
    assert txt_man.clean_up(in_str, [']', '[', '^', '-']) == (
        'Identity Number\n'
        '123456789\n'
        'Surname\n'
        'Doe\n'
        'Names\n'
        'JohnMichael\n'
        'Robert'
    )


def test_clean_up_invalid_arg_in_str():
    """
    Test that the clean up function raises the correct exception for an invalid in_str type.
    """
    txt_man = TextManager()
    with pytest.raises(TypeError):
        txt_man.clean_up(123)


def test_clean_up_invalid_arg_deplorables_1():
    """
    Test that the clean up function raises the correct exception for an invalid deplorables type.
    Particularly, checks to see if it is not a list.
    """
    txt_man = TextManager()
    with pytest.raises(TypeError):
        txt_man.clean_up('legit', 'not legit')


def test_clean_up_invalid_arg_deplorables_2():
    """
    Test that the clean up function raises the correct exception for an invalid deplorables type.
    Particularly, checks to see if it is not a list of srings.
    """
    txt_man = TextManager()
    with pytest.raises(TypeError):
        txt_man.clean_up('', [1.1, 2.2, 3.3])


def test_clean_up_invalid_arg_deplorables_3():
    """
    Test that the clean up function raises the correct exception for an invalid deplorables type.
    Particularly, checks to see if it is not a list of srings.
    """
    txt_man = TextManager()
    with pytest.raises(TypeError):
        txt_man.clean_up('', ['almost', 'but not quite', 3.3])


def test_clean_up_invalid_arg_append_deplorables():
    """
    Test that the clean up function raises the correct exception for an invalid append_deplorables type.
    """
    txt_man = TextManager()
    with pytest.raises(TypeError):
        txt_man.clean_up('', ['quite', 'legit'], None)


def test_dictify_empty_in_str():
    """
    Test the case in which an empty string is passed to the dictify function.
    """
    txt_man = TextManager()
    assert txt_man.dictify('') == {
        'identity_number': None,
        'surname': None,
        'names': None,
        'sex': None,
        'date_of_birth': None,
        'country_of_birth': None,
        'status': None,
        'nationality': None
    }


def test_dictify_default_skip_unnecessary():
    """
    Test the dictify function's ability to search for relevant (pre-specified) information.
    """
    txt_man = TextManager()
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
    assert txt_man.dictify(in_str) == {
        'identity_number': None,
        'surname': 'Doe',
        'names': 'John-Michael Robert',
        'sex': 'M',
        'date_of_birth': '13 Jan 1971',
        'country_of_birth': 'RSA',
        'status': 'Citizen',
        'nationality': 'RSA'
    }


def test_dictify_default_id_num_found():
    """
    Test the case in which an ID number was found by dictify and whether it is used to extract other information
    such as date of birth, status and sex.
    """
    txt_man = TextManager()
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
    assert txt_man.dictify(in_str) == {
        'identity_number': '7101135111011',
        'surname': 'Doe',
        'names': 'John-Michael Robert',
        'sex': 'M',
        'date_of_birth': '71-01-13',
        'country_of_birth': 'RSA',
        'status': 'Citizen',
        'nationality': 'RSA'
    }


def test_dictify_default_id_num_found_same_line():
    """
    Test the case in which an ID number was found, on the same line as the ID number field name, by dictify and
    whether it is used to extract other information such as date of birth, status and sex.
    """
    txt_man = TextManager()
    in_str = (
        'Id no 7101135111011\n'
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
    assert txt_man.dictify(in_str) == {
        'identity_number': '7101135111011',
        'surname': 'Doe',
        'names': 'John-Michael Robert',
        'sex': 'M',
        'date_of_birth': '71-01-13',
        'country_of_birth': 'RSA',
        'status': 'Citizen',
        'nationality': 'RSA'
    }


def test_dictify_default_id_num_not_found():
    """
    Test the case in which an ID number was not found by dictify.
    """
    txt_man = TextManager()
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
    assert txt_man.dictify(in_str) == {
        'identity_number': None,
        'surname': 'Doe',
        'names': 'John-Michael Robert',
        'sex': 'M',
        'date_of_birth': '13 Jan 1971',
        'country_of_birth': 'RSA',
        'status': 'Hungry',
        'nationality': 'RSA'
    }


def test_dictify_id_in_barcode():
    """
    Test the case in which an ID number was extracted from a barcode and passed to dictify and whether it is used to
    extract other information such as date of birth, status and sex.
    """
    txt_man = TextManager()
    in_str = (
        'Identity Number\n'
        '123456789\n'
        'Surname\n'
        'Doe\n'
        'Names\n'
        'Jane-Michael\n'
        'Robert'
    )
    assert txt_man.dictify(in_str, barcode_data={'identity_number': '7101134111111'}) == {
        'identity_number': '7101134111111',
        'surname': 'Doe',
        'names': 'Jane-Michael Robert',
        'sex': 'F',
        'date_of_birth': '71-01-13',
        'country_of_birth': None,
        'status': 'Non Citizen',
        'nationality': None
    }


def test_dictify_multi_line_1():
    """
    Test the ability of the dictify function to retrieve field values over multiple lines.
    This case checks for a maximum of 2 lines.
    """
    txt_man = TextManager()
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
    assert txt_man.dictify(in_str) == {
        'identity_number': '7101135111011',
        'surname': 'Doe',
        'names': 'John-Michael Robert',
        'sex': 'M',
        'date_of_birth': '71-01-13',
        'country_of_birth': None,
        'status': 'Citizen',
        'nationality': None
    }


def test_dictify_multi_line_2():
    """
    Test the ability of the dictify function to retrieve field values over multiple lines.
    This case checks if a match to multi_line_end was found.
    """
    txt_man = TextManager()
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
    assert txt_man.dictify(in_str) == {
        'identity_number': '7101135111011',
        'surname': 'Doe',
        'names': 'John-Michael',
        'sex': 'M',
        'date_of_birth': '71-01-13',
        'country_of_birth': None,
        'status': 'Citizen',
        'nationality': None
    }


def test_dictify_multi_line_3():
    """
    Test the ability of the dictify function to retrieve field values over multiple lines.
    This case checks how a specified multi_line field value is dealt with if the value does not exist at the end of
    the in_string.
    """
    txt_man = TextManager()
    in_str = (
        'Names'
    )
    assert txt_man.dictify(in_str) == {
        'identity_number': None,
        'surname': None,
        'names': None,
        'sex': None,
        'date_of_birth': None,
        'country_of_birth': None,
        'status': None,
        'nationality': None
    }


def test_dictify_bare_multi_line_4():
    """
    Test the ability of the dictify function to retrieve field values over multiple lines.
    This case checks how a specified multi_line field value is dealt with if the value exists, but is at the end of
    the in_string.
    """
    txt_man = TextManager()
    in_str = (
        'Surname\n'
        'Doe\n'
        'Names\n'
        'John\n'
        'Robert'
    )
    assert txt_man.dictify(in_str, max_multi_line=4) == {
        'identity_number': None,
        'surname': 'Doe',
        'names': 'John Robert',
        'sex': None,
        'date_of_birth': None,
        'country_of_birth': None,
        'status': None,
        'nationality': None
    }


def test_dictify_max_multi_line():
    """
    Test the ability of the dictify function to retrieve field values over multiple lines.
    This case checks if the correct number of multi_line was considered when specified.
    """
    txt_man = TextManager()
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
    assert txt_man.dictify(in_str, max_multi_line=3) == {
        'identity_number': '7101135111011',
        'surname': 'Doe',
        'names': 'John-Michael Robert Douglas',
        'sex': 'M',
        'date_of_birth': '71-01-13',
        'country_of_birth': None,
        'status': 'Citizen',
        'nationality': None
    }


def test_dictify_fuzzy_1():
    """
    Tests to see if dictify is capable of retrieving field values through reasonable or commonly required fuzzy
    matching to be performed.
    """
    txt_man = TextManager()
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
    assert txt_man.dictify(in_str) == {
        'identity_number': '7101135111011',
        'surname': 'Doe',
        'names': 'John-Michael Robert',
        'sex': 'M',
        'date_of_birth': '71-01-13',
        'country_of_birth': None,
        'status': 'Citizen',
        'nationality': 'RSA'
    }


def test_dictify_fuzzy_2():
    """
    Tests to see if dictify is capable of retrieving field values through reasonable or commonly required fuzzy
    matching to be performed.
    """
    txt_man = TextManager()
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
    assert txt_man.dictify(in_str) == {
        'identity_number': '7101135111011',
        'surname': 'Doe',
        'names': 'John-Michael Robert',
        'sex': 'M',
        'date_of_birth': '71-01-13',
        'country_of_birth': None,
        'status': 'Citizen',
        'nationality': 'RSA'
    }


def test_dictify_fuzzy_min_ratio():
    """
    Tests the dictify function fuzzy matching with a specified minimum ratio.
    """
    txt_man = TextManager()
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
    assert txt_man.dictify(in_str, fuzzy_min_ratio=90) == {
        'identity_number': None,
        'surname': 'Doe',
        'names': 'John-Michael Robert',
        'sex': 'M',
        'date_of_birth': None,
        'country_of_birth': None,
        'status': None,
        'nationality': None
    }


def test_dictify_bare():
    """
    Test the dictify function's behaviour when a field name is matched, but no field value follows and is at the end
    of the in_string.
    """
    txt_man = TextManager()
    in_str = (
        'Surname\n'
    )
    assert txt_man.dictify(in_str) == {
        'identity_number': None,
        'surname': None,
        'names': None,
        'sex': None,
        'date_of_birth': None,
        'country_of_birth': None,
        'status': None,
        'nationality': None
    }


def test_dictify_invalid_arg_in_str():
    """
    Test to see if dictify raises the correct exception when an incorrect type for the in_str arg is passed.
    """
    txt_man = TextManager()
    with pytest.raises(TypeError):
        txt_man.dictify(['not legit'])


def test_dictify_invalid_arg_barcode_data():
    """
    Test to see if dictify raises the correct exception when an incorrect type for the barcode_data arg is passed.
    """
    txt_man = TextManager()
    with pytest.raises(TypeError):
        txt_man.dictify('seems legit', 'nope')
