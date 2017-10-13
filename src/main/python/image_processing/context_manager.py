"""
This file contains the logic used to manage the various ID contexts.
Should ideally be extended to do more than it currently does.
"""

from id_contexts.sa_id_card import SAIDCard
from id_contexts.sa_id_book import SAIDBook
from id_contexts.sa_id_book_old import SAIDBookOld
from id_contexts.up_student_card import UPStudentCard

__author__ = "Jan-Justin van Tonder"
__copyright__ = "Copyright 2017, Java the Hutts"
__license__ = "BSD"
__maintainer__ = "Jan-Justin van Tonder"
__email__ = "J.vanTonder@tuks.co.za"
__status__ = "Development"


class ContextManager:
    """
    A class responsible for managing and maintaining the various ID contexts.

    Attributes:
        _sa_id_card (IDContext): A South African ID card context.
        _sa_id_book (IDContext): A South African ID book context.
        _sa_id_book_old (IDContext): An old South African ID book context.
        _up_card (IDContext): A University of Pretoria staff/student card context.
    """
    def __init__(self):
        """
        Responsible for initialising the ContextManager object.
        """
        # Create ID contexts to manage and maintain.
        self._sa_id_card = SAIDCard()
        self._sa_id_book = SAIDBook()
        self._sa_id_book_old = SAIDBookOld()
        self._up_card = UPStudentCard()

    def get_id_context(self, id_type):
        """
        Returns an ID context based on the ID type that is passed in as an arg.

        Args:
            id_type (str): A string indicating a type of ID.

        Returns:
            (IDContext): An IDContext object determined by the ID type passed in as an arg.
            (None): In the event that the ID type is unrecognisable.
        """
        # Determine which ID context to return, otherwise return None.
        if id_type == 'idcard':
            return self._sa_id_card
        elif id_type == 'idbook':
            return self._sa_id_book
        elif id_type == 'idbookold':
            return self._sa_id_book_old
        elif id_type == 'studentcard':
            return self._up_card
        return None
