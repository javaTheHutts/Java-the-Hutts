"""
----------------------------------------------------------------------
Authors: Jan-Justin van Tonder
----------------------------------------------------------------------
Contains the logic used to verify the extracted text from a form
of ID.
----------------------------------------------------------------------
"""

import Levenshtein
from hutts_utils.hutts_logger import logger, prettify_json_message


class TextVerify:
    """
    This class is responsible for the verification of text that is extracted from an ID.

    Authors:
        Jan-Justin van Tonder
    """
    def __init__(self):
        """
        Initialises the TextVerify object.

        Authors:
            Jan-Justin van Tonder
        """
        # Logging for debugging purposes.
        logger.debug('Initialising TextVerify...')

    def verify(self, extracted, verifier, threshold=0.75, min_matches=4, verbose=False):
        """
        This function is responsible for the verification of text that is extracted from an ID and is passed in,
        along with information that is to be used to verify the extracted text.

        Args:
            extracted (dict): A dictionary containing the information that was extracted from an ID.
            verifier (dict): A dictionary containing the information against which the extracted data is to be
                verified.
            threshold (float): A threshold decimal value that is used to determine whether or not the final match
                percentage is accepted as verified.
            min_matches (int): The minimum number of matches that have to be calculated for the final result to be
                considered as verified.
            verbose (bool): Indicates whether or not to return all of the calculated match percentages.

        Returns:
            (bool, float | dict): The first value returned is a bool that indicates whether or not the total
                percentage match is above the specified threshold value, while the second return value is the total
                percentage match value if verbose is False, or returns a dict of all the determined percentage match
                values if verbose is True.
        """
        if type(extracted) is not dict:
            raise TypeError('Bad type for arg extracted - expected dict. Received type ' + str(type(extracted)))
        if type(verifier) is not dict:
            raise TypeError('Bad type for arg verifier - expected dict. Received type ' + str(type(verifier)))
        if type(threshold) is not float:
            raise TypeError('Bad type for arg threshold - expected float. Received type ' + str(type(threshold)))
        if type(min_matches) is not int:
            raise TypeError('Bad type for arg min_matches - expected int. Received type ' + str(type(min_matches)))
        if type(verbose) is not bool:
            raise TypeError('Bad type for arg verbose - expected bool. Received type ' + str(type(verbose)))
        # Set minimum number of matches, if zero or less set to one.
        min_matches = min_matches if min_matches > 0 else 1
        min_percentage = threshold * 100
        # Logging for debugging and verbose purposes.
        logger.debug('Threshold for verification set as: ' + str(min_percentage))
        logger.debug('Minimum number of matches for verification set as: ' + str(min_matches))
        logger.debug('Simplified percentages to be returned' if not verbose else 'Verbose percentages to be returned')
        logger.debug('Verifying:')
        # Prettify and log the extracted information.
        [logger.debug(log_line) for log_line in prettify_json_message(extracted).split('\n')]
        logger.debug('Against:')
        # Prettify and log the verifier information.
        [logger.debug(log_line) for log_line in prettify_json_message(verifier).split('\n')]
        # Initialise a dictionary to house the final matching percentages.
        match_percentages = {}
        # Iterate over the verifier and calculate a percentage match for the values,
        # if the keys match and the corresponding values exist.
        for key, value in verifier.items():
            if key in extracted and extracted[key]:
                logger.debug('Computing match "' + str(value) + '" and "' + str(extracted[key]) + '"...')
                match_percentages[key] = self._match_percentage(value, extracted[key])
                logger.debug('"' + value + '" and "' + extracted[key] + '" match percentage is : ' +
                             str(match_percentages[key]))
            else:
                logger.warning('Could not find corresponding field "' + key + '" in extracted information to verify')
        # Determine the number of percentages calculated and initialise a default value for the total match score.
        num_scores = len(match_percentages)
        total_match_percentage = 0.0
        # Check if enough matches were found.
        if num_scores >= min_matches:
            # Calculate the total match score.
            total_match_percentage = self._total_percentage_match(match_percentages)
        # Either the minimum number of percentages criteria was not met.
        else:
            logger.warning('A total of ' + str(num_scores) + ' matches were found, which is less than the minimum')
        # Determine whether or not the text is verified.
        is_verified = total_match_percentage >= min_percentage
        # Logging for debugging purposes.
        logger.debug('Intermediate match percentages:')
        [logger.debug(log_line) for log_line in prettify_json_message(match_percentages).split('\n')]
        logger.debug('Final match percentage: ' + str(total_match_percentage))
        logger.debug('Threshold to pass: ' + str(min_percentage))
        logger.debug('Result: ' + 'Passed' if is_verified else 'Failed')
        # Return the final result.
        if not verbose:
            return is_verified, total_match_percentage
        # Append the total to the existing percentages for verbose, and return all percentage values.
        match_percentages['total'] = total_match_percentage
        return is_verified, match_percentages

    @staticmethod
    def _match_percentage(str_x, str_y):
        """
        This function is responsible for determining the percentage match for two strings and returning
        said percentage.

        Authors:
            Jan-Justin van Tonder

        Args:
            str_x (str): The first string that is used to perform matching.
            str_y (str): The second string that is used to perform matching.

        Returns:
            (float): Match percentage of the two given strings.

        Raises:
            TypeError: If str_x is not a string.
            TypeError: If str_y is not a string.
        """
        if type(str_x) is not str:
            raise TypeError('Bad type for arg str_x - expected string. Received type ' + str(type(str_x)))
        if type(str_y) is not str:
            raise TypeError('Bad type for arg str_y - expected string. Received type ' + str(type(str_y)))
        return Levenshtein.ratio(str_x, str_y) * 100

    @staticmethod
    def _total_percentage_match(matches):
        """
        This function is responsible for calculating a single, total percentage match value for a dict of match
        values that have been calculated.

        Authors:
            Jan-Justin van Tonder

        Args:
            matches (dict): A dictionary of pre-calculated, match percentages.

        Returns:
            (float): A total match percentage (out of 100) for a given set of match percentages.

        Todo:
            Investigate the proposal of calculating a weighted total.
        """
        return sum(matches.values()) / len(matches)
