"""
Wraps functions that are used to simplify or ease the image processing process.
"""

import cv2
import os
import imutils
import numpy as np
from imutils.perspective import four_point_transform
from hutts_verification.utils.hutts_logger import logger

__author__ = "Nicolai van Niekerk, Stephan Nell"
__copyright__ = "Copyright 2017, Java the Hutts"
__license__ = "BSD"
__maintainer__ = "Nicolai van Niekerk"
__email__ = "nicvaniek@gmail.com"
__status__ = "Development"

DESKTOP = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')
# The minimum contour area must be to be transformed.
CONTOUR_AREA_THRESHOLD = 150000


class SimplificationManager:
    """
    The Simplification manger is used to remove unwanted content in an image thus
    simplifying process like OCR and facial comparisons.
    """

    def perspectiveTransformation(self, image, use_io):
        """
        The perspective transformation takes the image passed and applies edge detection and
        a function to detect the contours of a identification document. If contours of an
        identification document is detected the image is converted from a non-perspective view
        to a perspective view.

        :param image (obj): Image containing a identification document.
        :param use_io (boolean): Whether or not to write images to disk.

        Returns:
            - (obj): The transformed image.

        Raises:
            - TypeError: If a parameter is passed that is not of type Numpy array.

        """
        if not isinstance(image, np.ndarray):
            raise TypeError(
                'Bad type for arg image - expected image in numpy array. Received type "%s".' %
                type(image).__name__
            )

        ratio = image.shape[0] / 500.0
        orig = image.copy()
        image = imutils.resize(image, height=500)

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (5, 5), 0)
        edged = cv2.Canny(gray, 75, 200)
        if use_io:
            cv2.imwrite(DESKTOP + "/output/1.png", edged)
        (_, contours, _) = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:5]
        warped = orig
        # Used to prevent false positive detection
        logger.debug('Contour area Threshold: ' + str(cv2.contourArea(contours[0])))
        if cv2.contourArea(contours[0]) > CONTOUR_AREA_THRESHOLD:
            for c in contours:
                peri = cv2.arcLength(c, True)
                approx = cv2.approxPolyDP(c, 0.02 * peri, True)

                if len(approx) == 4:
                    screen_contours = approx
                    break

            cv2.drawContours(image, [screen_contours], -1, (0, 255, 0), 2)
            if use_io:
                cv2.imwrite(DESKTOP + "/output/2.png", image)
            logger.debug('Performing four point simplification')
            warped = four_point_transform(orig, screen_contours.reshape(4, 2) * ratio)
        return warped
