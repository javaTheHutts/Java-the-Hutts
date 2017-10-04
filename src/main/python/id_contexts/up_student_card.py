"""
----------------------------------------------------------------------
Authors: Jan-Justin van Tonder
----------------------------------------------------------------------
This file contains the logic for University of Pretoria ID
card context. It is mainly intended for demonstration purposes.
----------------------------------------------------------------------
"""

import re
from id_contexts.id_context import IDContext
from hutts_utils.hutts_logger import logger


class UPStudentCard(IDContext):
    """
    A class that represents an ID context for a University of Pretoria ID card.
    """
    def __init__(self):
        """
        Initialises the UPStudentCard object.
        """
        # Logging for debugging purposes.
        logger.debug('Initialising %s...' % type(self).__name__)
        # Initialise parent
        IDContext.__init__(self, [])

    def _dictify(self, match_contexts, id_string, barcode_data, fuzzy_min_ratio, max_multi_line):
        """
        This function is responsible for generating a dictionary object containing the relevant ID information,
        such as names, surname, ID number, etc., from a given input string containing said relevant information.
        In this particular ID context, the information is sparse and is mainly intended for demonstration purposes.

        Authors:
            Jan-Justin van Tonder

        Args:
            match_contexts (list): A list of dictionaries that contain the contextual information used in the process
                of retrieving field values from the OCR output string - not particularly useful for this ID context.
            id_string (str): A string containing some ID information.
            barcode_data (dict, Optional): A dictionary object containing information extracted from a barcode.
            fuzzy_min_ratio (float): The threshold ratio for a minimum, acceptable ratio of fuzziness when comparing
                two strings.
            max_multi_line (int): Specifies the maximum number of lines that is to be extracted from fields that are
                noted as running onto multiple lines.

        Returns:
            (dict): A dictionary object containing the relevant, extracted ID information.
        """
        id_info = {}
        regexp = re.compile(r'[0-9]{6,10}')
        for line_index, line in enumerate(id_string.split('\n')):
            is_match = re.match(regexp, line)
            if is_match:
                # Populate id_info with the student/staff number.
                id_info['identity_number'] = re.sub('[^\d]', '', line)
                # Retrieve some more information from the previous line.
                if line_index - 1 >= 0:
                    # Split the line on spaces.
                    id_line = id_string[line_index - 1].split(' ')
                    # Attempt to extrapolate sex.
                    sex = 'M' if id_line[0] == 'Mr' else None
                    sex = 'M' if id_line[0] == 'Ms' else sex
                    # Attempt to get initials
                    id_line.pop(0)
                    initials = id_line[0]
                    # Re-combine the rest of the list to get the surname.
                    id_line.pop(0)
                    surname = ' '.join(id_line)
                    # Populate the id_info list to be returned.
                    if sex is not None:
                        id_info['sex'] = sex
                    id_info['names'] = initials
                    id_info['surname'] = surname
                break
        # Check if barcode data is available.
        if barcode_data and barcode_data['identity_number']:
            id_info['identity_number'] = barcode_data['identity_number']
        return id_info
