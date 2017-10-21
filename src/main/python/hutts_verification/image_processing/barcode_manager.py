"""
A class that is responsible for detecting a barcode and extracting information
from said barcode.
"""

import numpy as np
import cv2
import zbar.misc

__author__ = "Stephan Nell"
__copyright__ = "Copyright 2017, Java the Hutts"
__license__ = "BSD"
__maintainer__ = "Stephan Nell"
__email__ = "nellstephanj@gmail.com"
__status__ = "Development"


# The minimum area a rectangle must be to be considered a barcode.
BOUNDING_RECTANGLE_THRESHOLD = 200


class BarCodeManager:
    """
    The BarCode Manager is responsible for:

    1. Detecting the barcode.
    2. Extracting any information on the detected barcode.
    3. Applying blurring to the detected barcode to reduce noise.

    """

    def __init__(self):
        self.scanner = zbar.Scanner()

    def detect(self, image):
        """
        This function detects a region containing a barcode if a barcode is present in the image passed.
        Barcodes supported:

            - EAN
            - UPC
            - Code 39
            - Code 93
            - Code 128
            - ITF

        For more information on Barcode types: https://www.scandit.com/types-barcodes-choosing-right-barcode/.

        :param image (obj): Image containing the potential barcode.

        Returns:
            - (boolean): Indicates whether a barcode was detected or not.
            - (obj): Return the detected barcode or the original image, based on whether the barcode was found.
            - (int list): This list contains the box coordinates for the region in which the barcode resides.

        Raises:
            - TypeError: If a none numpy array value has been passed.

        """
        if type(image) is not np.ndarray:
            raise TypeError(
                'Bad type for arg image - expected image in numpy array. Received type "%s".' %
                type(image).__name__
            )
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        grad_x = cv2.Sobel(gray, ddepth=cv2.CV_32F, dx=1, dy=0, ksize=-1)
        grad_y = cv2.Sobel(gray, ddepth=cv2.CV_32F, dx=0, dy=1, ksize=-1)

        gradient = cv2.subtract(grad_x, grad_y)
        gradient = cv2.convertScaleAbs(gradient)

        blurred = cv2.blur(gradient, (7, 7))
        (_, thresh) = cv2.threshold(blurred, 225, 255, cv2.THRESH_BINARY)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (27, 7))
        closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

        eroded = cv2.erode(closed, None, iterations=4)
        dilated = cv2.dilate(eroded, None, iterations=4)

        (_, contours, _) = cv2.findContours(dilated.copy(), cv2.RETR_EXTERNAL,
                                            cv2.CHAIN_APPROX_SIMPLE)
        c = sorted(contours, key=cv2.contourArea, reverse=True)[0]

        rectangle = cv2.minAreaRect(c)
        box = cv2.boxPoints(rectangle)
        box = np.int0(box)
        (x, y, w, h) = cv2.boundingRect(box)
        # The Difference between the upper and lower Y-value is calculated to ensure a Barcode is detected.
        # This reduces the chance of a false positive detection.
        diff = y - (y+h)
        if abs(diff) < BOUNDING_RECTANGLE_THRESHOLD:
            return True, image[y:y + h, x:x + w], box
        else:
            return False, image, box

    def get_barcode_info(self, image):
        """
        This function returns scanned barcode information.

        :param image (obj): Image containing a Barcode.

        Returns:
            - (boolean): Whether the function was able to extract information from the barcode.
            - (str): A UTF-8 String of the data extracted from the barcode (empty if nothing was extracted).
            - (obj): A copy of the original image.

        """
        (detection, detected_image, box) = self.detect(image.copy())
        if detection:
            gray = cv2.cvtColor(detected_image, cv2.COLOR_BGR2GRAY)
            results = self.scanner.scan(gray)
            if not results:
                return False, "", image
            else:
                image = self.apply_barcode_blur(image, box)
                return True, results[0].data, image
        else:
            return False, "", image

    def apply_barcode_blur(self, image, box, dilation_intensity=2):
        """
        This function applies blurring to a detected barcode region to reduce noise in the image.
        The barcode region is first extracted, then blurring is applied, after blurring is applied
        the blurred out barcode is reapplied to the original image.

        :param image (obj): Image containing a Barcode.
        :param box (int list): The box is an integer list containing the box region coordinates of the
                barcode location.
        :param dilation_intensity (int): Indicates the intensity by which the barcode should be dilated.
                The greater the intensity the greater the extent of dilation.

        Returns:
             (obj): The original image with blurring applied to the barcode region in the image.

        """
        (x, y, w, h) = cv2.boundingRect(box)
        sub_bar_code = image[y:y + h, x:x + w]
        sub_bar_code = cv2.dilate(sub_bar_code, None, iterations=dilation_intensity)
        sub_bar_code = cv2.GaussianBlur(sub_bar_code, (31, 31), 0)
        image[y:y + sub_bar_code.shape[0], x:x + sub_bar_code.shape[1]] = sub_bar_code
        return image
