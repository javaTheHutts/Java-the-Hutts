"""
This file contains the abstraction and high-level logic of South
African ID contexts.
"""

import re
from abc import abstractmethod
from fuzzywuzzy import fuzz
from datetime import datetime
from hutts_verification.id_contexts.id_context import IDContext, LineType
from hutts_verification.utils.hutts_logger import logger

__authors__ = "Jan-Justin van Tonder, Stephan Nell, Marno Hermann"
__copyright__ = "Copyright 2017, Java the Hutts"
__license__ = "BSD"
__maintainer__ = "Jan-Justin van Tonder"
__email__ = "J.vanTonder@tuks.co.za"
__status__ = "Development"


class SAID(IDContext):
    """
    An abstract class for South African IDs.
    Contains the high-level logic that is relevant to all South African IDs.
    """
    # Define a class-level constant for a minimum fuzzy ratio during post-processing.
    POST_PROCESS_MIN_FUZZY_RATIO = 70.0

    # Define a class-level constant for a valid ID number length.
    VALID_ID_LENGTH = 13

    # Define a class-level constant as a minimum age year delta for year threshold.
    MIN_AGE_DELTA = 15

    # Define a class-level constant as a year delta for year threshold.
    YEAR_DELTA = 100

    def __init__(self, match_contexts):
        """
        Initialises the SAID object.

        :param match_contexts (list): A list of dictionaries that contain the contextual
                information used in the process of retrieving field values from the OCR output string.

        """
        # Logging for debugging purposes.
        logger.debug('Initialising %s...' % type(self).__name__)
        # Initialise parent.
        IDContext.__init__(self, match_contexts)

    def _dictify(self, match_contexts, id_string, barcode_data, fuzzy_min_ratio, max_multi_line):
        """
        This function is responsible for generating a dictionary object containing the relevant ID information,
        such as names, surname, ID number, etc., from a given input string containing said relevant information.

        :param match_contexts (list): A list of dictionaries that contain the contextual information used
                in the process of retrieving field values from the OCR output string.
        :param id_string (str): A string containing some ID information.
        :param barcode_data (dict): A dictionary object containing information extracted from a barcode.
        :param fuzzy_min_ratio (float): The threshold ratio for a minimum, acceptable ratio of fuzziness
                when comparing two strings.
        :param max_multi_line (int): Specifies the maximum number of lines that is to be extracted from
                fields that are noted as running onto multiple lines.

        Returns:
            - (dict): A dictionary object containing the relevant, extracted ID information.
        """
        # Given a string containing extracted ID text,
        # create a dictionary object and populate it with
        # relevant information from said text.
        id_info = {}
        # Check if barcode data, containing the id number, exists and
        # if so, save it and extract some relevant information from it.
        # It should overwrite any existing fields that can be extracted from the id number, since
        # the information embedded within the id number is more reliable, at least theoretically.
        if barcode_data:
            logger.debug('Extracting details from barcode data...')
            id_info['identity_number'] = barcode_data['identity_number']
            self._id_number_information_extraction(match_contexts, id_info, barcode_data['identity_number'])
        # Attempt to populate id_info with information from the given ID string.
        logger.debug('Extracting details from the given text string...')
        self._populate_id_information(match_contexts, id_string, id_info, fuzzy_min_ratio, max_multi_line)
        # Perform some custom post-processing on the information that was extracted.
        logger.debug('Post-processing some field values...')
        self._post_process(id_info)
        # Return the info that was found.
        return id_info

    def _populate_id_information(self, match_contexts, id_string, id_info, fuzzy_min_ratio, max_multi_line):
        """
        This function is responsible for populating a dictionary object with information that it is able to find
        and extract from a given string containing ID information.

        :param id_string (str): A string containing some ID information.
        :param id_info (dict): A dictionary object used to house extracted ID information.
        :param fuzzy_min_ratio (float): The threshold ratio for a minimum, acceptable ratio of fuzziness when
                comparing two strings.
        :param max_multi_line (int): Specifies the maximum number of lines that is to be extracted from fields
                that are noted as running onto multiple lines.

        """
        # Split the id_string on the newline character to generate a list.
        id_string_list = id_string.split('\n')
        # Attempt to retrieve matches.
        for match_context in match_contexts:
            # Extract desired field name from context as key.
            key = match_context['field']
            # Only retrieve information if it does not exist or it could not previously
            # be determined.
            if key not in id_info or not id_info[key]:
                id_info[key] = self._get_match(id_string_list, match_context, fuzzy_min_ratio, max_multi_line)
                # If the ID number has been retrieved, use it to extract other useful information.
                # It should overwrite any existing fields that can be extracted from the id number, since
                # the information embedded within the id number is more reliable, at least theoretically.
                if key == 'identity_number' and id_info[key]:
                    self._id_number_information_extraction(match_contexts, id_info, id_info[key])

    def _get_match(self, id_string_list, match_context, fuzzy_min_ratio, max_multi_line):
        """
        This function is responsible for searching through a list of lines from an ID string and extracting the
        relevant ID information based on some context for image_processing that is provided as input. Fuzzy string
        matching is performed on field names in order to extract field values. This process is assisted with a context
        that is is to be provided.

        :param id_string_list (list): An ID string that has been broken down into a list of individual lines.
        :param match_context (dict): A dictionary object that provides context for the information that is to be
                extracted.
        :param fuzzy_min_ratio (float): The threshold ratio for a minimum, acceptable ratio of fuzziness when
                comparing two strings.
        :param max_multi_line (int): Specifies the maximum number of lines that is to be extracted from fields
                that are noted as running onto multiple lines.

        Returns:
            - (str): A string containing the extracted information, if a match was found.
            - (None): If nothing was matched or an extracted value is an empty string.
        """
        best_match_ratio = fuzzy_min_ratio
        match = None
        skip_to_index = -1
        id_num_lines = len(id_string_list)
        # Set the most suitable fuzzy matching function based on line type.
        get_match_ratio = fuzz.token_set_ratio
        if match_context['line_type'] == LineType.TITLED_ADJACENT:
            get_match_ratio = fuzz.partial_token_set_ratio
        # Iterate over the id_string list to find fuzzy matches.
        for current_index, current_line in enumerate(id_string_list):
            # Check to see if we can jump ahead and ignore the current index.
            if skip_to_index > current_index:
                continue
            # Is there a match?
            match_ratio = get_match_ratio(current_line, match_context['find'])
            if match_ratio >= best_match_ratio:
                # Set new best match ratio and retrieve the info if possible
                best_match_ratio = match_ratio
                # Check for special cases of extraction.
                idiosyncratic_match = self._get_idiosyncratic_match(match_context, id_string_list, current_index)
                if idiosyncratic_match is not None:
                    match = idiosyncratic_match
                # Check to see if we are dealing with a field value on single line adjacent to the field name.
                elif match_context['line_type'] == LineType.TITLED_ADJACENT:
                    match = re.sub(match_context['find'], '', current_line).strip()
                # Check to see if we are going out of bounds of the string before proceeding.
                elif match_context['line_type'] == LineType.TITLED_NEWLINE and current_index + 1 < id_num_lines:
                    # We are only interested in field value, not field name.
                    # e.g: Surname\n
                    #      Smith\n
                    #      ...
                    # ignore 'Surname' so as to be able to manually specify field name
                    # in the context settings.
                    # Retrieve the field value on the very next line.
                    match = id_string_list[current_index + 1]
                    # If the field value exists over multiple lines.
                    if match_context['multi_line']:
                        # Determine the lower bound index for field values that span multiple lines.
                        lower_index = current_index + 2
                        if lower_index >= id_num_lines:
                            # There is nothing to find in this case.
                            continue
                        # Determine the upper bound index for field values that span multiple lines.
                        upper_index = current_index + max_multi_line + 1
                        if upper_index > id_num_lines:
                            # Don't go out of bounds.
                            upper_index = id_num_lines
                        # Iterate ahead to retrieve the field value that spans over multiple lines.
                        for forward_index in range(lower_index, upper_index):
                            # For ech of the specified endpoints, check if the end of the field value has
                            # been reached.
                            end_point_ratio = fuzz.token_set_ratio(
                                match_context['multi_line_end'],
                                id_string_list[forward_index]
                            )
                            if end_point_ratio >= fuzzy_min_ratio:
                                skip_to_index = forward_index
                                break
                            # Otherwise, add the line to the field value.
                            match += ' %s' % id_string_list[forward_index].strip()
                # Check if a legitimate match was found before proceeding.
                if not match:
                    continue
                # Normalise the match found.
                match = self._normalise_match(match_context, match)
        # Final check to see if an empty string ('', not None) is the match found, return None if this is the case.
        if not match:
            return None
        # Otherwise return what we have found.
        return match

    @abstractmethod
    def _get_idiosyncratic_match(self, match_context, id_string_list, current_index):
        """
        Abstract method to be implemented by subclasses.
        Meant to retrieve matches that are particular to a context of a subclass.

        :param match_context (dict): A dictionary object that provides context for the information that
                is to be extracted.
        :param id_string_list (list): An ID string that has been broken down into a list of individual lines.
        :param current_index (int): The current index within the ID string list.

        """
        pass

    @staticmethod
    def _id_number_information_extraction(match_contexts, id_info, id_number):
        """
        This function is responsible for extracting information from a given ID number and populating a given
        dictionary object with the extracted information.

        :param match_contexts (list): A list of dictionaries that contain the contextual information used in
                the process of retrieving field values from the OCR output string.
        :param id_info (dict): A dictionary object containing extracted ID information.
        :param id_number (str): An ID number.

        """
        for match_context in match_contexts:
            if match_context['field'] == 'date_of_birth':
                # Extract date of birth digits from ID number.
                yy = id_number[:2]
                mm = id_number[2:4]
                dd = id_number[4:6]
                # Populate id_info with date of birth.
                date_of_birth = '%s-%s-%s' % (yy, mm, dd)
                id_info['date_of_birth'] = date_of_birth
            if match_context['field'] == 'sex':
                # Extract gender digit from ID Number.
                gender_digit = id_number[6:7]
                # Populate id_info with gender info.
                # Currently, the genders on South African IDs are binary, meaning an individual is
                # either male or female.
                id_info['sex'] = 'F' if gender_digit < '5' else 'M'
            if match_context['field'] == 'status':
                # Extract status digit from ID Number.
                status_digit = id_number[10:11]
                # Populate id_info with status info.
                id_info['status'] = 'Citizen' if status_digit == '0' else 'Non Citizen'

    def _post_process(self, id_info):
        """
        Used to perform custom processing after extraction has taken place.
        All custom operations that are required after all the extraction has taken place, should be
        called from within this function.

        :param id_info (dict): A dictionary object used to house extracted ID information.

        Returns:
            - (dict): The original id_info, with some post-processed field values.

        """
        # Check if date of birth field exists for post-processing.
        if 'date_of_birth' in id_info and id_info['date_of_birth']:
            id_info['date_of_birth'] = self._standardise_date_of_birth(id_info['date_of_birth'])
        # Check if country of birth field exists for post-processing.
        if 'country_of_birth' in id_info and id_info['country_of_birth']:
            fuzz_ratio = fuzz.token_set_ratio(id_info['country_of_birth'], 'SUID-AFRIKA')
            # We should be fairly certain, with a margin for error, that we have a match.
            if fuzz_ratio >= SAID.POST_PROCESS_MIN_FUZZY_RATIO:
                # Translate from Afrikaans to English
                id_info['country_of_birth'] = 'South Africa'

    @staticmethod
    def _standardise_date_of_birth(date_of_birth):
        """
        Standardises the date of birth field value due to a mixture of formats that can be extracted.
        Due to the preference of extracting the date of birth from the id number as opposed to
        the OCR output, there tends to be a discrepancy in the date format retrieved, therefore,
        standardise it for future use.

        :param date_of_birth (str): The date of birth to be standardised.

        Returns:
            - (str): A standardised date of birth field value if the extracted format could be parsed, else the
                extracted format is kept.

        """
        try:
            # Attempt to parse the different dates that could appear for formatting.
            current_date_of_birth = re.sub(' ', '', date_of_birth)
            # If the current date contains a '-', then it was extracted from the id number and '-' is the
            # third character in, parse it in the format 'YY-MM-DD'
            if '-' in current_date_of_birth and current_date_of_birth.index('-') == 2:
                standardised_date_of_birth = datetime.strptime(current_date_of_birth, '%y-%m-%d')
            # If the current date contains a '-', then it was extracted from the id number, parse it in the
            # format 'YYYY-MM-DD' based on elimination of possibilities for this specific ID context.
            elif '-' in current_date_of_birth:
                standardised_date_of_birth = datetime.strptime(current_date_of_birth, '%Y-%m-%d')
            # Otherwise it was extracted from the OCR output, therefore, parse it in the
            # format 'DD MMM YYYY'
            else:
                standardised_date_of_birth = datetime.strptime(current_date_of_birth, '%d%b%Y')
            # Check to see if the year is too far in the future.
            threshold_year = datetime.now().year - SAID.MIN_AGE_DELTA
            if standardised_date_of_birth.year >= threshold_year:
                # Reduce the year by a defined year delta.
                replacement_year = standardised_date_of_birth.year - SAID.YEAR_DELTA
                standardised_date_of_birth = standardised_date_of_birth.replace(year=replacement_year)
            # Standardise the date by formatting it according to ISO date format standard,
            # which is 'YYYY-MM-DD'
            return datetime.strftime(standardised_date_of_birth, '%Y-%m-%d')
        except ValueError:
            # Could not parse the date so log and keep it as is.
            logger.warning('Could not parse date "%s" for formatting. Keeping date as is.' % date_of_birth)
            return date_of_birth

    def validate_id_number(self, id_number):
        """
        Determines whether a given id number is valid or not.

        :param id_number (str): An ID number that is to be validated.

        Returns:
            - (bool): True if the id number is valid, False otherwise.

        Raises:
            - TypeError: If id_number is not a string containing only numeric characters.

        """
        if (not isinstance(id_number, str)) or (isinstance(id_number, str) and not id_number.isnumeric()):
            raise TypeError(
                'Bad type for arg id_number - expected string of ONLY numeric characters. Received type "%s"' %
                type(id_number).__name__
            )
        # Logging for debugging purposes.
        logger.debug('Checking if ID number is valid...')
        # Determine if the id number is of a valid length.
        is_valid_length = len(id_number) == SAID.VALID_ID_LENGTH
        logger.debug('ID number length appears %s' % ('valid' if is_valid_length else 'invalid'))
        # Return early since the result will be false anyways.
        # Do not calculate the checksum if it is not required.
        if not is_valid_length:
            logger.debug('ID number appears invalid')
            return False
        # Determine if the id number checksum is valid.
        is_valid_id_checksum = self._compute_checksum(id_number) == 0
        # Both the length and the checksum must be valid for the entire id number to be valid.
        is_valid_id_number = is_valid_length and is_valid_id_checksum
        # Logging for debugging purposes.
        logger.debug('ID number checksum appears %s' % ('valid' if is_valid_id_checksum else 'invalid'))
        logger.debug('ID number appears %s' % ('valid' if is_valid_id_number else 'invalid'))
        # Return final result of validation.
        return is_valid_id_number

    @staticmethod
    def _compute_checksum(id_number):
        """
        Compute the Luhn checksum for the given id number string for validation.

        :param id_number (str): A string containing an id number for which the Luhn checksum is to be calculated.

        Returns:
            - (int): Luhn checksum value for validation.

        """
        # Create a list of ID number digits parsed as integers.
        digits = [int(digit) for digit in id_number]
        # Create a sum of the even digits by multiplying each digit by 2, performing mod 10 division and summing
        # the resultant digits.
        even_partial_sum = [sum(divmod(2 * digit, 10)) for digit in digits[-2::-2]]
        even_sum = sum(even_partial_sum)
        # Sum all the odd positioned digits.
        odd_sum = sum(digits[-1::-2])
        # Return the Luhn checksum value for validation.
        return (even_sum + odd_sum) % 10
