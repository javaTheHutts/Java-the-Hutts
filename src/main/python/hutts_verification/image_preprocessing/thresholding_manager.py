"""
Wraps all the functions related to applying thresholding techniques to an image.
"""

import cv2
import numpy as np

__authors__ = "Stephan Nell, Nicolai van Niekerk"
__copyright__ = "Copyright 2017, Java the Hutts"
__license__ = "BSD"
__maintainer__ = "Stephan Nell"
__email__ = "nellstephanj@gmail.com"
__status__ = "Development"


class ThresholdingManager:
    """
    The Thresholding manager is responsible for applying the different types of thresholding techniques.
    """
    def __init__(self, thresholding_type):
        """
        Initialise Thresholding manager.

        :param thresholding_type (str): Indicates the type of thresholding that should be applied.

        Raises:
            - TypeError: If a parameter is passed that is not of type String.
            - NameError: If the thresholding type is not Adaptive or Otsu.

        """
        if not isinstance(thresholding_type, str):
            raise TypeError(
                'Bad type for arg thresholding_type - expected string. Received type "%s".' %
                type(thresholding_type).__name__
            )

        if thresholding_type == "adaptive":
            self.thresholding_type = thresholding_type
        elif thresholding_type == "otsu":
            self.thresholding_type = thresholding_type
        else:
            raise NameError('Invalid Thresholding Selection! Try "adaptive" or "otsu" thresholding types.')

    def apply(self, image):
        """
        This performs the thresholding based on the predefined technique.

        :param image: The image to which the thresholding must be applied.

        Raises:
            - NameError: If a thresholding type other than 'adaptive' or 'otsu' is provided.

        Returns:
            - (obj): The image, with the appropriate thresholding applied to it.

        """
        if self.thresholding_type == "adaptive":
            return self.adaptiveThresholding(image)
        elif self.thresholding_type == "otsu":
            return self.otsuThresholding(image)
        else:
            raise NameError('Invalid Thresholding Selection! Could not Apply Thresholding')

    @staticmethod
    def adaptiveThresholding(image):
        """
        This function applies a simple adaptive thresholding to the image passed.

        :param image (obj): Image to which thresholding should be applied.

        Raises:
            - TypeError: If a parameter is passed that is not of type Numpy array.

        Returns:
            - (obj): The image, with adaptive thresholding applied to it.

        """
        if not isinstance(image, np.ndarray):
            raise TypeError(
                'Bad type for arg image - expected image in numpy array. Received type "%s".' %
                type(image).__name__
            )

        return cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 10)

    @staticmethod
    def otsuThresholding(image):
        """
        This function applies a simple Binary Inverse Otsu thresholding to the image passed.

        :param image (obj): Image to which thresholding should be applied.

        Raises:
            - TypeError: If a parameter is passed that is not of type Numpy array.

        Returns:
            - (obj): The image, with otsu thresholding applied to it.

        """
        if not isinstance(image, np.ndarray):
            raise TypeError(
                'Bad type for arg image - expected image in numpy array. Received type "%s".' %
                type(image).__name__
            )

        (_, threshInv) = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
        return threshInv
