"""
Contains the logic used to verify the extracted text from a form of ID.
"""

import Levenshtein
from hutts_verification.utils.hutts_logger import logger, prettify_json_message

__author__ = "Jan-Justin van Tonder"
__copyright__ = "Copyright 2017, Java the Hutts"
__license__ = "BSD"
__maintainer__ = "Jan-Justin van Tonder"
__email__ = "J.vanTonder@tuks.co.za"
__status__ = "Development"


class TextVerify:
    """
    This class is responsible for the verification of text that is extracted from an ID.
    """

    def __init__(self):
        """
        Initialises the TextVerify object.
        """
        # Logging for debugging purposes.
        logger.debug('Initialising %s...' % type(self).__name__)

    def verify(self, extracted, verifier, threshold=75.00, min_matches=4, verbose=False):
        """
        This function is responsible for the verification of text that is extracted from an ID and is passed in,
        along with information that is to be used to verify the extracted text.

        :param extracted (dict): The information that was extracted from an ID.
        :param verifier (dict): The information against which the extracted data is to be verified.
        :param threshold (float): A percentage used to determine if the match percentage is accepted as verified.
        :param min_matches (int): The minimum number of matches needed to allow a positive match.
        :param verbose (boolean): Indicates whether or not to return all of the calculated match percentages.

        Returns:
            - ((bool, float) | dict): The first value returned is a bool that indicates whether or not the total
                percentage match is above the specified threshold value, while the second return value is the total
                percentage match value if verbose is False, or returns a dict of all the determined percentage match
                values if verbose is True.

        Raises:
            TypeError: If any parameter is not of the correct type.

        """
        if not isinstance(extracted, dict):
            raise TypeError(
                'Bad type for arg extracted - expected dict. Received type "%s"' %
                type(extracted).__name__
            )
        if not isinstance(verifier, dict):
            raise TypeError(
                'Bad type for arg verifier - expected dict. Received type "%s"' %
                type(verifier).__name__
            )
        if not isinstance(threshold, float):
            raise TypeError(
                'Bad type for arg threshold - expected float. Received type "%s"' %
                type(threshold).__name__
            )
        if not isinstance(min_matches, int):
            raise TypeError(
                'Bad type for arg min_matches - expected int. Received type "%s"' %
                type(min_matches).__name__
            )
        if not isinstance(verbose, bool):
            raise TypeError(
                'Bad type for arg verbose - expected bool. Received type "%s"' %
                type(verbose).__name__
            )
        # Set minimum number of matches, if zero or less set to one.
        min_matches = min_matches if min_matches > 0 else 1
        # Logging for debugging and verbose purposes.
        logger.debug('Threshold for verification set as: %.2f' % threshold)
        logger.debug('Minimum number of matches for verification set as: %d' % min_matches)
        logger.debug('Simplified percentages to be returned' if not verbose else 'Verbose percentages to be returned')
        logger.debug('-' * 50)
        logger.debug('Verifying:')
        logger.debug('-' * 50)
        # Prettify and log the extracted information.
        [logger.debug(log_line) for log_line in prettify_json_message(extracted).split('\n')]
        logger.debug('-' * 50)
        logger.debug('Against:')
        logger.debug('-' * 50)
        # Prettify and log the verifier information.
        [logger.debug(log_line) for log_line in prettify_json_message(verifier).split('\n')]
        logger.debug('-' * 50)
        # Initialise a dictionary to house the final matching percentages.
        match_percentages = {}
        # Iterate over the verifier and calculate a percentage match for the values,
        # if the keys match and the corresponding values exist.
        for key, value in verifier.items():
            if key in extracted and extracted[key] is not None:
                # Compute the match percentage.
                logger.debug('Computing match "%s" and "%s"...' % (value, extracted[key]))
                match_percentages[key] = {
                    'match_percentage': self._match_percentage(value, extracted[key]),
                    'verifier_field_value': value,
                    'extracted_field_value': extracted[key]
                }
                logger.debug(
                    '"%s" and "%s" match percentage: %.2f' %
                    (value, extracted[key], match_percentages[key]['match_percentage'])
                )
            else:
                logger.warning('Could not find corresponding field "%s" in extracted information to verify' % key)
        # Determine the number of percentages calculated and initialise a default value for the total match score.
        num_scores = len(match_percentages)
        total_match_percentage = 0.0
        # Check if enough matches were found.
        if num_scores >= min_matches:
            # Calculate the total match score.
            total_match_percentage = self._total_percentage_match(match_percentages)
        # Either the minimum number of percentages criteria was not met.
        else:
            logger.warning('A total of %d matches were found, which is less than the minimum' % num_scores)
        # Determine whether or not the text is verified.
        is_verified = total_match_percentage >= threshold
        # Logging for debugging purposes.
        logger.debug('-' * 50)
        logger.debug('Intermediate match percentages:')
        logger.debug('-' * 50)
        [logger.debug(log_line) for log_line in prettify_json_message(match_percentages).split('\n')]
        logger.debug('-' * 50)
        logger.debug('Final match percentage: %.2f' % total_match_percentage)
        logger.debug('Threshold to pass: %.2f' % threshold)
        logger.debug('Result: ' + 'Passed' if is_verified else 'Failed')
        # Return the final result.
        if not verbose:
            return is_verified, total_match_percentage
        # Append the total and non-matches to the existing percentages for verbose purposes,
        # and return all percentage values.
        match_percentages.update(self._get_non_matches(extracted, verifier))
        match_percentages['total'] = total_match_percentage
        return is_verified, match_percentages

    @staticmethod
    def _match_percentage(str_x, str_y):
        """
        This function is responsible for determining the percentage match for two strings and returning
        said percentage.

        :param str_x (str): The first string that is used to perform matching.
        :param str_y (str): The second string that is used to perform matching.

        Returns:
            - (float): Match percentage of the two given strings.

        Raises:
            TypeError: If either parameter is not a string.
        """
        if not isinstance(str_x, str):
            raise TypeError(
                'Bad type for arg str_x - expected string. Received type "%s"' %
                type(str_x).__name__
            )
        if not isinstance(str_y, str):
            raise TypeError(
                'Bad type for arg str_y - expected string. Received type "%s"' %
                type(str_y).__name__
            )
        return round(Levenshtein.ratio(str_x, str_y) * 100, 2)

    @staticmethod
    def _total_percentage_match(matches):
        """
        This function is responsible for calculating a single, total percentage match value for a dict of match
        values that have been calculated.

        :param matches (dict): A dictionary of pre-calculated, match percentages.

        Returns:
            - (float): A total match percentage for a given set of match percentages.

        """
        return round(sum(value['match_percentage'] for value in matches.values()) / len(matches), 2)

    @staticmethod
    def _get_non_matches(extracted, verifier):
        """
        Creates a dictionary containing fields for which matches could not be computed, due to non-existence
        of fields or field values.

        :param extracted (dict): A dictionary containing the information that was extracted from an ID.
        :param verifier (dict): A dictionary containing the information against which the extracted data is to be
                verified.

        Returns:
            - (dict): A dictionary containing fields for which no matches can be found.

        """
        non_matches = {}
        # Iterate over the extracted and verifier dictionaries to determine the field values for which match
        # percentages cannot be computed due to non-existence of values.
        for (verify_key, verify_value), (extract_key, extract_value) in zip(verifier.items(), extracted.items()):
            # There exists no corresponding field or field value for the verifier in the extracted ID info.
            if verify_key not in extracted or extracted[verify_key] is None:
                non_matches[verify_key] = {
                    'match_percentage': None,
                    'verifier_field_value': verify_value,
                    'extracted_field_value': None
                }
            # There exists no corresponding field or field value for the extracted ID info in the verifier.
            if extract_key not in verifier or verifier[extract_key] is None:
                non_matches[extract_key] = {
                    'match_percentage': None,
                    'verifier_field_value': None,
                    'extracted_field_value': extract_value
                }
        return non_matches

    def validate_id_number(self, id_number, valid_length=13):
        """
        Determines whether a given id number is valid or not.

        :param id_number (str): The ID number that has to be validated.
        :param valid_length (int): Specifies the length of a given id number to be considered as valid.

        Returns:
            - (boolean): True if the id number is valid, False otherwise.

        Raises:
            TypeError: If id_number is not a string containing only numeric characters.
            TypeError: If valid_length is not an integer.

        """
        if (not isinstance(id_number, str)) or (isinstance(id_number, str) and not id_number.isnumeric()):
            raise TypeError(
                'Bad type for arg id_number - expected string of ONLY numeric characters. Received type "%s"' %
                type(id_number).__name__
            )
        if not isinstance(valid_length, int):
            raise TypeError(
                'Bad type for arg valid_length - expected integer. Received type "%s"' %
                type(valid_length).__name__
            )
        # Logging for debugging purposes.
        logger.debug('Checking if extracted id number is valid...')
        # Determine if the id number is of a valid length.
        is_valid_length = len(id_number) == valid_length
        logger.debug('Extracted id number length appears %s' % ('valid' if is_valid_length else 'invalid'))
        # Return early since the result will be false anyways.
        # Do not calculate the checksum if it is not required.
        if not is_valid_length:
            logger.debug('Extracted id number appears invalid')
            return False
        # Determine if the id number checksum is valid.
        is_valid_id_checksum = self._compute_checksum(id_number) == 0
        # Both the length and the checksum must be valid for the entire id number to be valid.
        is_valid_id_number = is_valid_length and is_valid_id_checksum
        # Logging for debugging purposes.
        logger.debug('Extracted id number checksum appears %s' % ('valid' if is_valid_id_checksum else 'invalid'))
        logger.debug('Extracted id number appears %s' % ('valid' if is_valid_id_number else 'invalid'))
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
        # Map the digits of the given id number to new integers and create a list from said mapping.
        digits = list(map(int, id_number))
        # Create a sum of the even digits by multiplying each digit by 2, performing mod 10 division and summing
        # the resultant digits.
        even_partial_sum = [sum(divmod(2 * digit, 10)) for digit in digits[-2::-2]]
        even_sum = sum(even_partial_sum)
        # Sum all the odd positioned digits.
        odd_sum = sum(digits[-1::-2])
        # Return the Luhn checksum value for validation.
        return (even_sum + odd_sum) % 10
