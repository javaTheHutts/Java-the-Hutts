"""
This file contains the logic used to manage the removal of characters
from an input string.
"""

import re
from hutts_verification.utils.hutts_logger import logger

__author__ = "Jan-Justin van Tonder"
__copyright__ = "Copyright 2017, Java the Hutts"
__license__ = "BSD"
__maintainer__ = "Jan-Justin van Tonder"
__email__ = "J.vanTonder@tuks.co.za"
__status__ = "Development"


class TextCleaner:
    """
    This class is encapsulates the logic required to clean the OCR output string produced from an image of an ID.

    Attributes:
        _deplorables (list): A list of strings that contain characters that is to be filtered out from the OCR output
            string during string cleaning.
    """
    def __init__(self):
        """
        Responsible for initialising the TextCleaner object.
        """
        # Logging for debugging purposes.
        logger.debug('Initialising %s...' % type(self).__name__)
        # Specify initial list of undesirable characters.
        self._deplorables = ['_']

    def clean_up(self, in_string, deplorables=None):
        """
        This function serves to receive an input string, clean it up through removing undesirable characters and
        unnecessary whitespace, and to return the cleaned string.

        Args:
            in_string (str): The input string that is to be cleaned.
            deplorables (list, Optional): A list of characters that are to be filtered from the input string.

        Returns:
            str: A string that has been stripped of undesirable characters and unnecessary whitespace.

        Raises:
            TypeError: If in_string is not a string.
            TypeError: If deplorables is not a list of strings.
        """
        # Check if the correct argument types have been passed in.
        if not isinstance(in_string, str):
            raise TypeError(
                'Bad type for arg in_string - expected string. Received type "%s".' %
                type(in_string).__name__
            )
        if deplorables and (not isinstance(deplorables, list) or not isinstance(deplorables[0], str)):
            raise TypeError(
                'Bad type for arg deplorables - expected list of strings. Received type "%s".' %
                type(deplorables).__name__
            )
        # Remove undesirable characters, spaces and newlines.
        compiled_deplorable_re = self._compile_deplorables(deplorables)
        sanitised = re.sub(compiled_deplorable_re, '', in_string)
        # Remove empty lines in-between text-filled lines.
        stripped_and_sanitised = re.sub(r'(\n\s*\n)', '\n', sanitised)
        # Remove multiple spaces before and after text-filled line.
        clean_text = re.sub(r'(\s*\n\s*)', '\n', stripped_and_sanitised)
        # Remove multiple spaces in-between text-filled line.
        clean_text = re.sub(r'( +)', ' ', clean_text)
        # Lastly, strip the trailing and leading spaces.
        clean_text = clean_text.strip()
        # Return cleaned text.
        return clean_text

    def _compile_deplorables(self, deplorables):
        """
        This function is responsible for compiling a regex pattern that is used to filter out the characters that
        were deemed undesirable from a string.

        Args:
            deplorables (list): A list of characters that are to be filtered from the input string.

        Returns:
            A compiled regex pattern used to match undesirable characters in a string.
        """
        # Append to existing list of undesirable characters if there is a given list of
        # undesirable characters
        if deplorables is not None:
            # Escape and append the list of undesirable characters.
            self._deplorables += re.escape(''.join(deplorables))
        # Define a class of characters that we wish to keep for the regex
        # that is to be compiled.
        reg_exp = r'[^\w\d\s-]'
        # If the existing list of undesirable characters is not empty,
        # add the list of undesirable characters to the regex that is to be compiled.
        reg_exp += r'|[' + ''.join(self._deplorables) + ']'
        # Returned a compiled regular expression pattern to use for matching.
        return re.compile(reg_exp, re.UNICODE)
