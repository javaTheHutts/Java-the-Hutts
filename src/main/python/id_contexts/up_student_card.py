"""
----------------------------------------------------------------------
Authors: Jan-Justin van Tonder
----------------------------------------------------------------------
This file contains the logic for University of Pretoria ID
card context. It is mainly intended for demonstration purposes.
----------------------------------------------------------------------
"""

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

    def _dictify(self):
        pass
