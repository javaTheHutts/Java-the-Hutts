"""
Utility functions to manage image handling from given parameters.
"""

import cv2
import numpy as np
from imutils.convenience import url_to_image
from hutts_verification.utils.hutts_logger import logger

__author__ = "Stephan Nell"
__copyright__ = "Copyright 2017, Java the Hutts"
__license__ = "BSD"
__maintainer__ = "Stephan Nell"
__email__ = "nellstephanj@gmail.com"
__status__ = "Development"


def grab_image(path=None, stream=None, url=None):
    """
    This function grabs the image from URL, or image path and applies necessary changes to the grabbed
    images so that the image is compatible with OpenCV operation.

    Args:
        path (str): The path to the image if it reside on disk
        stream (str): A stream of text representing where on the internet the image resides
        url(str): Url representing a path to where an image should be fetched.

    Raises:
            ValueError: If no path stream or URL was found.

    Returns:
        (:obj:'OpenCV image'): Image that is now compatible with OpenCV operations.
    """
    # If the path is not None, then load the image from disk. Example: payload = {"image": open("id.jpg", "rb")}
    if path is not None:
        logger.debug("Grabbing from Disk")
        image = cv2.imread(path)

        if image is None:
            raise ValueError('Invalid Path. No image could be found.'
                             ' Either path is incorrect or image does not exist')
    # otherwise, the image does not reside on disk
    else:
        # If the URL is not None, then download the image
        if url is not None:
            # Example: "http://www.pyimagesearch.com/wp-content/uploads/2015/05/obama.jpg"
            # If URL is incorrect Urllib in imutils library will catch the error.
            logger.debug("Downloading image from URL")
            return url_to_image(url)
        # if the stream is not None, then the image has been uploaded
        elif stream is not None:
            logger.debug("Downloading from image stream")
            data = stream.read()
            image = np.asarray(bytearray(data), dtype="uint8")
            image = cv2.imdecode(image, cv2.IMREAD_COLOR)
            if image is None:
                raise ValueError('Invalid Path. No image could be found.'
                                 ' Either path is incorrect or image does not exist')
        else:
            raise ValueError('No valid method was found to grab image.'
                             ' Either path is incorrect or image does not exist')

    return image
