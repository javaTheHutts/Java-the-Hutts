"""
This file contains the logic for South African ID book (pre 1994)
context.
"""

from id_contexts.id_context import FieldType, LineType
from id_contexts.sa_id import SAID
from fuzzywuzzy import fuzz

__author__ = "Jan-Justin van Tonder"
__copyright__ = "Copyright 2017, Java the Hutts"
__license__ = "BSD"
__maintainer__ = "Jan-Justin van Tonder"
__email__ = "J.vanTonder@tuks.co.za"
__status__ = "Development"


class SAIDBookOld(SAID):
    """
    A class that represents an ID context for a South African ID book (pre 1994).
    It supplies some of the concrete information, such as the match contexts, to the classes higher up in inheritance
    hierarchy and implements abstract methods defined by its parent.
    """
    def __init__(self):
        """
        Initialises the SAIDBookOld object.
        """
        # Specify initial list of contexts for string image_processing when populating
        # the ID information dictionary to send as output.
        match_contexts = [{
            'field': 'identity_number',
            'find': 'id no',
            'field_type': FieldType.NUMERIC_ONLY,
            'line_type': LineType.TITLED_ADJACENT,
            'multi_line': False
        }, {
            'field': 'surname',
            'find': 'vansurname',
            'field_type': FieldType.TEXT_ONLY,
            'to_uppercase': False,
            'line_type': LineType.TITLED_NEWLINE,
            'multi_line': True,
            'multi_line_end': 'voornameforenames'
        }, {
            'field': 'names',
            'find': 'voornameforenames',
            'field_type': FieldType.TEXT_ONLY,
            'to_uppercase': False,
            'line_type': LineType.TITLED_NEWLINE,
            'multi_line': True,
            'multi_line_end': 'geboortedistrik of-land'
        }, {
            'field': 'sex',
            'find': 'sex',
            'field_type': FieldType.TEXT_ONLY,
            'to_uppercase': False,
            'line_type': LineType.TITLED_NEWLINE,
            'multi_line': False
        }, {
            'field': 'date_of_birth',
            'find': 'geboortedatum',
            'field_type': FieldType.DATE_HYPHENATED,
            'to_uppercase': False,
            'line_type': LineType.TITLED_ADJACENT,
            'multi_line': False
        }, {
            'field': 'country_of_birth',
            'find': 'district or country of birth',
            'field_type': FieldType.TEXT_ONLY,
            'to_uppercase': True,
            'line_type': LineType.TITLED_NEWLINE,
            'multi_line': False
        }, {
            'field': 'status',
            'find': 'saburgersacitizen',
            'field_type': FieldType.TEXT_ONLY,
            'to_uppercase': False,
            'line_type': LineType.UNTITLED_ADJACENT,
            'multi_line': False
        }]
        # Initialise parent
        SAID.__init__(self, match_contexts)

    def _get_idiosyncratic_match(self, match_context, id_string_list, current_index):
        """
        Identifies and returns matches that are specific to the current ID context.

        Args:
            match_context (dict): A dictionary object that provides context for the information that is to be extracted.
            id_string_list (list): An ID string that has been broken down into a list of individual lines.
            current_index (int): The current index within the ID string list.

        Returns:
            (str): A string containing the match value of a context-specific case.
            (None): Used to indicate that no special case was identified.
        """
        # If we are looking for the ID number and the last few characters of the line
        # are numeric, then the ID number is on the same line instead of a new line.
        if match_context['field'] == 'identity_number':
            return id_string_list[current_index]
        # Check for the status special case.
        if match_context['field'] == 'status':
            citizen_match_ratio = fuzz.token_set_ratio(id_string_list[current_index], 'saburgersacitizen')
            non_citizen_match_ratio = fuzz.token_set_ratio(id_string_list[current_index], 'niesaburgernonsacitizen')
            match = 'citizen' if citizen_match_ratio > non_citizen_match_ratio else 'non citizen'
            return match
        # Check for date of birth special case.
        if match_context['field'] == 'date_of_birth':
            return id_string_list[current_index]
        # Otherwise return an empty string to indicate that a special case was not identified.
        return None
