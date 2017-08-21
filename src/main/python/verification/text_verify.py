import Levenshtein
from server.hutts_logger import logger, prettify_json_message


class TextVerify:
    def __init__(self):
        logger.debug('Initialising TextVerify...')
        self.percentage_match = lambda str_x, str_y: Levenshtein.ratio(str_x, str_y) * 100
        self.total_match = lambda matches: sum(val for val in matches.values()) / len(matches)

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
                scores[key] = self.percentage_match(value, extracted[key])
                logger.debug('"' + value + '" and "' + extracted[key] + '" match percentage is : ' + str(scores[key]))
            else:
                logger.warning('Could not find corresponding field "' + key + '" in extracted information to verify')
        # Calculate the total match score.
        num_scores = len(scores)
        total_score = 0.0
        if num_scores >= min_matches and num_scores > 0:
            total_score = self.total_match(scores)
        else:
            logger.warning('A total of ' + str(num_scores) + ' was found, which is less than the minimum')
        # Return the final result
        if not verbose:
            return total_score >= min_percentage, total_score
        scores['total'] = total_score
        return total_score >= min_percentage, scores
