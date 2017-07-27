import numpy as np
import cv2
import zbar.misc


class BarCodeManager:
    """
    The BarCode Manager is responsible for:
    1. Detecting the barcode
    2. Extracting any information on the detected barcode.
    3. Applying blurring to the detected barcode to reduce noise.
    """
    def __init__(self):
        """
        Initialise the BarCode Detector.
        """
        print("Initialise BarCodeDetector")

    def detect(self, image):
        """
        This function detects a region containing a Barcode if a Barcode is present in the image passed
        Barcodes supported:
            EAN
            UPC
            Code 39
            Code 93
            Code 128
            ITF
        For more information on Barcode types: https://www.scandit.com/types-barcodes-choosing-right-barcode/
        Author(s):
            Stephan Nell
        Args:
            image (:obj:'OpenCV image'): Image containing the potential barcode
        Returns:
            Boolean: A value of True is returned if a Barcode was detected
                if however a barcode was not detected a value of false is returned.
            obj:'OpenCV image': If a Barcode was successfully detected the detected barcode is returned
                if a barcode was not detected return the original image.
            Integer List: This list contains the box coordinates for the region in which the barcode resides.
        Todo:
            Find a way to support PDF417 format.
            Find a way to remove the hardcoded 200 value.
            Add additional checks for invalid Barcodes.
        """
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
        # The Diffrence between the upper and lower Y-value is calculated to ensure a Barcode is detected.
        # This reduces the chance of a false positive detection.
        diff = y - (y+h)
        if abs(diff) < 200:
            return True, image[y:y + h, x:x + w], box
        else:
            return False, image, box

    def get_barcode_info(self, image):
        """
        This function returns scanned barcode information.
        Author(s):
            Stephan Nell
        Args:
            image (:obj:'OpenCV image'): Image containing a Barcode
        Returns:
            Boolean: A value of True if the function was able to extract information from the barcode.
                If no information was extracted from the barcode a value of False is returned
            String: A UTF-8 String containing the information extracted from the Barcode
                If no information was extracted from the barcode a empty string is returned
            obj:'OpenCV image': A copy of the original image.
        Todo:
            Find a way to support PDF417 format.
        """
        (detection, detected_image, box) = self.detect(image.copy())
        if detection:
            gray = cv2.cvtColor(detected_image, cv2.COLOR_BGR2GRAY)
            scanner = zbar.Scanner()
            print(gray)
            print(gray.shape)
            results = scanner.scan(gray)
            image = self.apply_barcode_blur(image, box)
            if not results:
                return False, "", image
            else:
                return True, results[0].data, image
        else:
            return False, "", image

    def apply_barcode_blur(self, image, box):
        """
        This function applies blurring to a detected barcode region to reduce noise in the image.
        The barcode region is first extracted, then blurring is applied, after blurring is applied
        the blurred out barcode is reapplied to the original image
        Author(s):
            Stephan Nell
        Args:
            image (:obj:'OpenCV image'): Image containing a Barcode
            box: The box is an integer list containing the box region coordinates of the barcode location
        Returns:
             obj:'OpenCV image': The Original image with blurring applied to the barcode region in the image.
        """
        (x, y, w, h) = cv2.boundingRect(box)
        sub_bar_code = image[y:y + h, x:x + w]
        sub_bar_code = cv2.dilate(sub_bar_code, None, iterations=3)
        sub_bar_code = cv2.GaussianBlur(sub_bar_code, (31, 31), 0)
        image[y:y + sub_bar_code.shape[0], x:x + sub_bar_code.shape[1]] = sub_bar_code
        return image
