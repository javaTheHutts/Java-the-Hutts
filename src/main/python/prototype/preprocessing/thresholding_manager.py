import cv2


class ThresholdingManager:
    """
    The Thresholding manager is responsible for applying the different types of thresholding techniques
    """
    def __init__(self):
        """
        Initialise the Thresholding manager
        """
        print("Initialise Thresholding Manager")

    def adaptiveThresholding(self, image):
        """
        This function applies a simple adaptive thresholding to the image passed.
        Author(s):
            Stephan Nell
        Args:
            image (:obj:'OpenCV image'): Image to which thresholding should be applied.
        Returns:
            obj:'OpenCV image': The Thresholded image.
        Todo:
            Applies some error checking if an image of an invalid file type was passed.
        """
        return cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 25, 15)

    def otsuThresholding(self, image):
        """
        This function applies a simple Binary Inverse Otso thresholding to the image passed.
        Author(s):
            Stephan Nell
        Args:
            image (:obj:'OpenCV image'): Image to which thresholding should be applied.
        Returns:
            obj:'OpenCV image': The Thresholded image.
        Todo:
            Applies some error checking if an image of an invalid file type was passed.
        """
        (_, threshInv) = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
        return threshInv
