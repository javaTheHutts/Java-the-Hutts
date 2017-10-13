"""
----------------------------------------------------------------------
Authors: Jan-Justin van Tonder
----------------------------------------------------------------------
Unit tests for the Text Cleaner module.
----------------------------------------------------------------------
"""

import pytest
from hutts_verification.image_processing.text_cleaner import TextCleaner


def test_clean_up_empty_in_str():
    """
    Test the case in which an empty string is passed to the cleanup function.
    """
    text_cleaner = TextCleaner()
    assert text_cleaner.clean_up('') == ''


def test_clean_up_unicode_support():
    """
    Test support for unicode characters in the cleanup function.
    """
    text_cleaner = TextCleaner()
    in_str = (
        'Identity Number\n'
        '123456789\n'
        'Surname\n'
        'Döe\n'
        'Names\n'
        'John-Micháel\n'
        'Robert'
    )
    assert text_cleaner.clean_up(in_str) == (
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
    text_cleaner = TextCleaner()
    in_str = (
        'Identity Number\n\n\n'
        '123456789\n'
        'Surname\n'
        'Doe\n\n'
        'Names\n\n'
        'John-Michael\n'
        'Robert\n'
    )
    assert text_cleaner.clean_up(in_str) == (
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
    text_cleaner = TextCleaner()
    in_str = (
        'Identity Number\n'
        '123456789\n'
        'Surname\n'
        'Doe\n'
        'Names\n'
        'John     Michael   Robert'
    )
    assert text_cleaner.clean_up(in_str) == (
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
    text_cleaner = TextCleaner()
    in_str = (
        'Identity #Number\n'
        '123456789...\n'
        '$Sur_name&\n'
        '\\/Doe.\n'
        'Names*\n'
        'John-Michae|l\n'
        'R%obert+'
    )
    assert text_cleaner.clean_up(in_str) == (
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
    text_cleaner = TextCleaner()
    in_str = (
        'Identity Number\n'
        '123456789\n'
        'Surname\n'
        'Döe\n'
        'Names\n'
        'John+Michael\n'
        'Robert'
    )
    assert text_cleaner.clean_up(in_str, ['+', 'ö']) == (
        'Identity Number\n'
        '123456789\n'
        'Surname\n'
        'De\n'
        'Names\n'
        'JohnMichael\n'
        'Robert'
    )


def test_clean_up_remove_specified_sanitise():
    """
    Test the clean up function's removal with an additional list of characters to remove, but tests to see if certain
    control characters used within the underlying regex, such as ], [, ^ and -, are escaped.
    """
    text_cleaner = TextCleaner()
    in_str = (
        'Identity Number\n'
        '123456789\n'
        'Surname\n'
        'Doe[^-]\n'
        'Names\n'
        'John-Michael\n'
        'Robert'
    )
    assert text_cleaner.clean_up(in_str, [']', '[', '^', '-']) == (
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
    text_cleaner = TextCleaner()
    with pytest.raises(TypeError):
        text_cleaner.clean_up(123)


def test_clean_up_invalid_arg_deplorables_1():
    """
    Test that the clean up function raises the correct exception for an invalid deplorables type.
    Particularly, checks to see if it is not a list.
    """
    text_cleaner = TextCleaner()
    with pytest.raises(TypeError):
        text_cleaner.clean_up('legit', 'not legit')


def test_clean_up_invalid_arg_deplorables_2():
    """
    Test that the clean up function raises the correct exception for an invalid deplorables type.
    Particularly, checks to see if it is not a list of strings.
    """
    text_cleaner = TextCleaner()
    with pytest.raises(TypeError):
        text_cleaner.clean_up('', [1.1, 2.2, 3.3])


def test_clean_up_invalid_arg_deplorables_3():
    """
    Test that the clean up function raises the correct exception for an invalid deplorables type.
    Particularly, checks to see if it is not a list of strings.
    """
    text_cleaner = TextCleaner()
    with pytest.raises(TypeError):
        text_cleaner.clean_up('', ['almost', 'but not quite', 3.3])
