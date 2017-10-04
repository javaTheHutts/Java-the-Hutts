from id_contexts.id_context import IDContext
from hutts_utils.hutts_logger import logger


class UPStudentCard(IDContext):
    def __init__(self, match_contexts):
        # Logging for debugging purposes.
        logger.debug('Initialising %s...' % type(self).__name__)
        # Initialise parent
        IDContext.__init__(self, match_contexts)

    def _dictify(self):
        pass
