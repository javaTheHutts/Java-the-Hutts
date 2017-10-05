"""
----------------------------------------------------------------------
Authors: Jan-Justin van Tonder
----------------------------------------------------------------------
This file contains the abstraction of all ID contexts, which contain
the necessary information and settings specific to a particular ID
document type.
----------------------------------------------------------------------
"""

import re
from abc import ABC, abstractmethod
from enum import Enum
from hutts_utils.hutts_logger import logger


class IDContext(ABC):
    """
    This class is an abstraction of all ID contexts.
    The ID contexts serve to contain the necessary information and settings specific to a particular ID
    document type for operations such as extracting information from an ID OCR string.

    Attributes:
        match_contexts (list): A list of dictionaries that contain the contextual information used in the process of
            retrieving field values from the OCR output string.
            e.g. {
                    'field': 'surname',          // The field name - can be set to any string one desires.
                    'find': 'surname',           // A string to be used for matching field names.
                                                 // in the OCR output string (used to know what to look for).
                    'field_type':                // Indicates if the field value is to be treated as alphanumeric or
                       FieldType.TEXT_ONLY       // just numeric or just alphabetical characters.
                                                 // (e.g. indicates that all numbers from field value should be removed
                                                 // if the field type is TEXT_ONLY).
                    'line_type': TITLED_NEWLINE  // Indicates the type of line to be considered when looking for the
                                                 // field value relative to the 'find' value.
                                                 // (e.g. TITLED_NEWLINE indicates that the field value is preceded
                                                 // by a field name/title and a newline).
                    'multi_line': True,          // Indicates that the field value spans multiple lines.
                    'multi_line_end': 'names'    // (Optional, unless multi_line is true) A string identifying the next
                                                 // field name that indicates the end of the multi-line field value.
                    'to_uppercase': False,       // (Optional) Indicates that the retrieved field value must be
                                                 // converted to uppercase.
               }
    """
    def __init__(self, match_contexts):
        """
        Responsible for initialising the IDContext object.

        Args:
            match_contexts (list): A list of dictionaries that contain the contextual information used in the process
                of retrieving field values from the OCR output string.
        """
        # Logging for debugging purposes.
        logger.debug('Initialising %s...' % type(self).__name__)
        # Assign match contexts
        self._match_contexts = match_contexts

    def get_id_info(self, id_string, barcode_data=None, ignore_fields=None, fuzzy_min_ratio=60.0, max_multi_line=2):
        """
        Responsible for filtering undesirable fields to be retrieved as well as delegating the responsibility
        of extracting ID information from an OCR string and housing said information in a convenient dictionary.
        Some type checking is done to reduce the likelihood of errors further down the call stack.

        Authors:
            Jan-Justin van Tonder

        Args:
            id_string (str): A string containing some ID information.
            barcode_data (dict, Optional): A dictionary object containing information extracted from a barcode.
            ignore_fields (list, Optional): A list containing fields which are to be ignored during extraction.
            fuzzy_min_ratio (float): The threshold ratio for a minimum, acceptable ratio of fuzziness when comparing
                two strings.
            max_multi_line (int): Specifies the maximum number of lines that is to be extracted from fields that are
                noted as running onto multiple lines.

        Returns:
            (dict): A dictionary object containing the relevant, extracted ID information.

        Raises:
            TypeError: If id_string is not a string.
            TypeError: If barcode_data is not a dictionary.
        """
        # Check if arguments passed in are the correct type.
        if type(id_string) is not str:
            raise TypeError(
                'Bad type for arg id_string - expected string. Received type "%s".' %
                type(id_string).__name__
            )
        if barcode_data and type(barcode_data) is not dict:
            raise TypeError(
                'Bad type for arg barcode_data - expected dictionary. Received type "%s".' %
                type(barcode_data).__name__
            )
        if ignore_fields and (type(ignore_fields) is not list or type(ignore_fields[0]) is not str):
            raise TypeError(
                'Bad type for arg ignore_fields - expected list of strings. Received type "%s".' %
                type(ignore_fields).__name__
            )
        if type(fuzzy_min_ratio) is not float:
            raise TypeError(
                'Bad type for arg fuzzy_min_ratio - expected float. Received type "%s".' %
                type(fuzzy_min_ratio).__name__
            )
        if type(max_multi_line) is not int:
            raise TypeError(
                'Bad type for arg max_multi_line - expected int. Received type "%s".' %
                type(max_multi_line).__name__
            )
        # Initialise a match context list for extraction.
        match_contexts = self._match_contexts[:]
        # Check if filtering is necessary.
        if ignore_fields is not None:
            # Filter out the fields that are to be ignored.
            match_contexts = self._filter_ignore_match_contexts(ignore_fields)
        # Extract ID information and house it in a dictionary, which is returned.
        return self._dictify(match_contexts, id_string, barcode_data, fuzzy_min_ratio, max_multi_line)

    def _filter_ignore_match_contexts(self, ignore_fields):
        """
        Filters out fields which are to be ignored from the match_contexts.

        Authors:
            Jan-Justin van Tonder

        Args:
            ignore_fields (list): A list containing fields which are to be ignored during extraction.

        Returns:
            (dict): A filtered list of match contexts.
        """
        filtered_match_contexts = []
        for match_context in self._match_contexts:
            if match_context['field'] not in ignore_fields:
                filtered_match_contexts.append(match_context)
        return filtered_match_contexts

    @abstractmethod
    def _dictify(self, match_contexts, id_string, barcode_data, fuzzy_min_ratio, max_multi_line):
        """
        Abstract method for subclasses to implement.
        Meant to extract ID information from a string and, possibly, barcode data, which is to be returned
        in a convenient dictionary format.

        Args:
            match_contexts (list): A list of dictionaries that contain the contextual information used in the process
                of retrieving field values from the OCR output string.
            id_string (str): A string containing some ID information.
            barcode_data (dict, Optional): A dictionary object containing information extracted from a barcode.
            fuzzy_min_ratio (float): The threshold ratio for a minimum, acceptable ratio of fuzziness when comparing
                two strings.
            max_multi_line (int): Specifies the maximum number of lines that is to be extracted from fields that are
                noted as running onto multiple lines.
        """
        pass

    @staticmethod
    def _normalise_match(match_context, match):
        """
        Normalises a given match string according to the context it was matched.

        Authors:
            Jan-Justin van Tonder

        Args:
            match_context (dict): A dictionary object that provides context for the information that is to be extracted.
            match (str): A string containing matched ID information.

        Returns:
            (str): A match string normalised according to its matched context.
        """
        # If the field value should only be text, strip everything that is numeric.
        if match_context['field_type'] == FieldType.TEXT_ONLY:
            match = re.sub(r'[^\w\s-]', '', match)
        # If the field value ought to be numeric only, strip everything that is not numeric.
        elif match_context['field_type'] == FieldType.NUMERIC_ONLY:
            match = re.sub(r'[^\d]', '', match)
        elif match_context['field_type'] == FieldType.DATE_HYPHENATED:
            match = re.sub(r'[^\d-]', '', match)
        # Check if conversion to uppercase was specified.
        if 'to_uppercase' in match_context and match_context['to_uppercase']:
            match = match.upper()
        # If the field value does not require to be converted to uppercase.
        elif 'to_uppercase' in match_context and not match_context['to_uppercase']:
            # Convert to lowercase and capitalise the character of each new word.
            match = match.lower().title()
        return match


class FieldType(Enum):
    """
    An enumerator used to specify the field type for extracted ID information.
    """
    TEXT_ONLY = 0
    NUMERIC_ONLY = 1
    MIXED = 2
    DATE_HYPHENATED = 3


class LineType(Enum):
    """
    An enumerator used to specify the line type for extracted ID information.
    """
    TITLED_NEWLINE = 0
    TITLED_ADJACENT = 1
    UNTITLED_NEWLINE = 2
    UNTITLED_ADJACENT = 3
