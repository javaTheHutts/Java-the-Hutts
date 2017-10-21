"""
----------------------------------------------------------------------
Authors: Jan-Justin van Tonder
----------------------------------------------------------------------
Unit tests for the context manager module.
----------------------------------------------------------------------
"""

from image_processing.context_manager import ContextManager
from id_contexts.id_context import IDContext


def test_get_id_context_known_1():
    """
    Test to see if an IDContext is returned when a known ID type is given.
    """
    context_manager = ContextManager()
    assert isinstance(context_manager.get_id_context('idcard'), IDContext)


def test_get_id_context_known_2():
    """
    Test to see if an IDContext is returned when a known ID type is given.
    """
    context_manager = ContextManager()
    assert isinstance(context_manager.get_id_context('idbook'), IDContext)


def test_get_id_context_known_3():
    """
    Test to see if an IDContext is returned when a known ID type is given.
    """
    context_manager = ContextManager()
    assert isinstance(context_manager.get_id_context('idbookold'), IDContext)


def test_get_id_context_known_4():
    """
    Test to see if an IDContext is returned when a known ID type is given.
    """
    context_manager = ContextManager()
    assert isinstance(context_manager.get_id_context('studentcard'), IDContext)


def test_get_id_context_none():
    """
    Test to see if None is returned when an unknown ID type is given.
    """
    context_manager = ContextManager()
    assert context_manager.get_id_context('uhhh... I dunno') is None
