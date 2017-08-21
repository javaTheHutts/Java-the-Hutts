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
    This class is responsible for the verification of text that is extracted from an ID
    and is passed in along with information that is to be used to verify the extracted
    text.

    Authors:
        Jan-Justin van Tonder
    """
    def __init__(self):
        """
        Initialises the TextVerify object.

        Authors:
            Jan-Justin van Tonder
        """
        logger.debug('Initialising TextVerify...')

    def verify(self, extracted, verifier, threshold=0.75, min_matches=3, verbose=False):
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
            logger.warning('A total of ' + str(num_scores) + ' was found, which is less than the minimum')
        # Return the final result
        if not verbose:
            return total_score >= min_percentage, total_score
        scores['total'] = total_score
        return total_score >= min_percentage, scores

    @staticmethod
    def _percentage_match(str_x, str_y):
        return Levenshtein.ratio(str_x, str_y) * 100

    @staticmethod
    def _total_match(matches):
        return sum(matches.values()) / len(matches)
