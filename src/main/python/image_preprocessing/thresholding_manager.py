import cv2


class ThresholdingManager:
    """
    The Thresholding manager is responsible for applying the different types of thresholding techniques.
    """
    def __init__(self, thresholding_type):
        """
        Initialise Thresholding manager.
        Authors(s):
            Nicolai van Niekerk, Stephan Nell
        Args:
            thresholding_type (str): Indicates the type of thresholding that
                should be applied.
        Returns:
            None

        """
        self.thresholding_type = thresholding_type

    def apply(self, image):
        """
        This performs the thresholding based on the predefined technique.
        Author(s):
            Nicolai van Niekerk, Stephan Nell
        Args:
            image: The image to which the thresholding must be applied.
        Raises:
            NameError: If invalid thresholding type is provided. i.e. Adaptive or Otsu.
        Returns:
            obj:'OpenCV image': The threshold image.
        """
        if self.thresholding_type == "adaptive":
            return self.adaptiveThresholding(image)
        elif self.thresholding_type == "otsu":
            return self.otsuThresholding(image)
        else:
            raise NameError('Invalid Thresholding Selection! Try "Adaptive" or "Otsu" thresholding types.')

    def adaptiveThresholding(self, image):
        """
        This function applies a simple adaptive thresholding to the image passed.
        Author(s):
            Stephan Nell
        Args:
            image (:obj:'OpenCV image'): Image to which thresholding should be applied.
        Returns:
            obj:'OpenCV image': The Threshold image.
        Todo:
            Applies some error checking if an image of an invalid file type was passed.

        """
        return cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 10)

    def otsuThresholding(self, image):
        """
        This function applies a simple Binary Inverse Otso thresholding to the image passed.
        Author(s):
            Stephan Nell
        Args:
            image (:obj:'OpenCV image'): Image to which thresholding should be applied.
        Returns:
            obj:'OpenCV image': The Threshold image.
        Todo:
            Applies some error checking if an image of an invalid file type was passed.

        """
        (_, threshInv) = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
        return threshInv
