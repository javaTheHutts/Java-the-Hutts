"""
Utilities to help solve Python path/directory/file issues regarding files being
installed in either the dist-packages or the site-packages folder.
"""

from pathlib import Path
from hutts_verification.utils.hutts_logger import logger

__author__ = "Andreas Nel"
__copyright__ = "Copyright 2017, Java the Hutts"
__license__ = "BSD"
__maintainer__ = "Andreas Nel"
__email__ = "nel.andreas1@gmail.com"
__status__ = "Development"


def correct_path(path):
    """
    This function checks if the given path exists in most known
    Python package installation directories and returns the corresponding path.

    Args:
        path (string || Path): The path that has to be checked.

    Returns:
        string : The correct path if it exists, else None.
    """
    search_path = Path(path)
    logger.debug("Looking for " + str(search_path))
    result = ""
    try:
        if search_path.exists():
            result = search_path
        elif "dist-packages" in search_path.parts:
            result = _transform_path(search_path, "dist-packages", "site-packages")
        elif "site-packages" in search_path.parts:
            result = _transform_path(search_path, "site-packages", "dist-packages")
        logger.debug("Result is: " + str(result))
        logger.debug("Result exists: " + str(result.exists()))
        return str(result) if result.exists() else None
    except Exception:
        return None


def _transform_path(path, search_str, replace_str):
    """
    This function replaces a single directory in the given path by the given string and returns the new path.

    Args:
        path (string || Path): The path that has to be transformed.
        search_str (string): The directory that has to be changed.
        replace_str (string): The directory that the subdirectory has to be changed to.

    Returns:
        Path : The new path if the replacement was successful, else the original path.
    """
    result = Path(path)
    subdirectories = list(path.parts)
    if search_str in subdirectories:
        subdirectories[subdirectories.index(search_str)] = replace_str
        result = Path(*subdirectories)
    return result
