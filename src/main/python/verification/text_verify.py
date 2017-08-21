"""
----------------------------------------------------------------------
Authors: Jan-Justin van Tonder
----------------------------------------------------------------------
Contains the logic used to verify the extracted text from a form
of ID.
----------------------------------------------------------------------
"""

import Levenshtein
from server.hutts_logger import logger, prettify_json_message


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

    def verify(self, extracted, verifier, threshold=0.75, min_matches=3, verbose=False):
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
        min_percentage = threshold * 100
        # Logging for debugging and verbose purposes.
        logger.debug('Threshold for verification set as: ' + str(min_percentage))
        logger.debug('Minimum number of matches for verification set as: ' + str(min_matches))
        logger.debug('Simplified scores to be returned' if not verbose else 'Verbose scores to be returned')
        logger.debug('Verifying:')
        # Prettify and log the extracted information.
        [logger.debug(log_line) for log_line in prettify_json_message(extracted).split('\n')]
        logger.debug('Against:')
        # Prettify and log the verifier information.
        [logger.debug(log_line) for log_line in prettify_json_message(verifier).split('\n')]
        # Initialise a dictionary to house the final matching percentages.
        scores = {}
        # Iterate over the verifier and calculate a percentage match for the values,
        # if the keys match and the corresponding values exist.
        for key, value in verifier.items():
            if key in extracted and extracted[key]:
                logger.debug('Computing match "' + value + '" and "' + extracted[key] + '"...')
                scores[key] = self._percentage_match(value, extracted[key])
                logger.debug('"' + value + '" and "' + extracted[key] + '" match percentage is : ' + str(scores[key]))
            else:
                logger.warning('Could not find corresponding field "' + key + '" in extracted information to verify')
        # Determine the number of scores calculated and initialise a default value for the total match score.
        num_scores = len(scores)
        total_score = 0.0
        # Check if enough matches were found.
        if num_scores >= min_matches and num_scores > 0:
            # Calculate the total match score.
            total_score = self._total_match(scores)
        # Either the minimum number of scores criteria was not met, or their were no matches at all.
        else:
            logger.warning('A total of ' + str(num_scores) + ' was found, which is less than the minimum or is zero')
        # Return the final result
        if not verbose:
            return total_score >= min_percentage, total_score
        scores['total'] = total_score
        return total_score >= min_percentage, scores

    @staticmethod
    def _percentage_match(str_x, str_y):
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
        """
        return Levenshtein.ratio(str_x, str_y) * 100

    @staticmethod
    def _total_match(matches):
        """
        This function is responsible for calculating a single, total percentage match value for a dict of match
        values that have been calculated.

        Authors:
            Jan-Justin van Tonder

        Args:
            matches (dict): A dictionary of pre-calculated, match percentages.

        Returns:
            (float): A total match percentage for a given set of match percentages.
        """
        return sum(matches.values()) / len(matches)
