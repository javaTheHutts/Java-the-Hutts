"""
Utility functions to manage image handling from given parameters.
"""

import cv2
import numpy as np
import base64
from imutils.convenience import url_to_image
from hutts_verification.utils.hutts_logger import logger

__authors__ = "Stephan Nell, Andreas Nel"
__copyright__ = "Copyright 2017, Java the Hutts"
__license__ = "BSD"
__maintainer__ = "Stephan Nell"
__email__ = "nellstephanj@gmail.com"
__status__ = "Development"


def grab_image(path=None, stream=None, url=None, string=None):
    """
    This function grabs the image from URL, or image path and applies necessary changes to the grabbed
    images so that the image is compatible with OpenCV operation.

    :param str (path): The path to the image if it resides on disk.
    :param str (stream): A stream of text representing an image upload.
    :param str (url): URL representing a path to where an image should be fetched.
    :param str (string): A base64 encoded string of the image.

    Raises:
        - ValueError: If no path, stream, URL or Base64 string was found.

    Returns:
        - (obj): Image that is now compatible with OpenCV operations.

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
        # If string is not None, then the image was transmitted with base64 encoding.
        elif string is not None:
            logger.debug("Decoding base64 string")
            encoded_data = string.split(',')[1]
            nparr = np.fromstring(base64.b64decode(encoded_data), np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
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
