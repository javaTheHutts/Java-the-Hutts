import cv2
import numpy as np


class ColorManager:
    """
    The Color manager is responsible for applying several color management techniques
    to image passed.
    """
    def __init__(self, type, channel="green", kernel_size=(13, 7)):
        """
        Initialise the Colour Manager
        """
        self.type = type
        self.channel = channel
        self.kernel_size = kernel_size

        print("Initialise Color Manager")

    def apply(self, image):
        """
        This performs the specified processing technique
        Author(s):
            Nicolai van Niekerk
        Args:
            image: The image to which the technique must be applied
        Returns:
            obj:'OpenCV image': The modified image
        Todo:
        """
        if self.type == "histogram":
            return self.histEqualisation(image)
        elif self.type == "extract":
            return self.extractChannel(image, self.channel)
        elif self.type == "blackHat":
            return self.blackHat(image, self.kernel_size)
        elif self.type == "topHat":
            return self.topHat(image, self.kernel_size)

    def histEqualisation(self, image):
        """
        This function applies histogram equalisation to the image passed
        Author(s):
            Stephan Nell
        Args:
            image (:obj:'OpenCV image'): Image to which histogram equalisation should be applied to.
        Returns:
            obj:'OpenCV image': The Histogram equalised image.
        """
        return cv2.equalizeHist(image)

    def extractChannel(self, image, image_channel="green"):
        """
        This function extracts a selected color channel from an image.
        Author(s):
            Stephan Nell
        Args:
            image (:obj:'OpenCV image'): Image to which image channel should be removed
            str: Color that should be removed valid color red, green, blue
        Raises:
            NameError: If invalid colour is selected i.e. not red, green, blue
        Returns:
            obj:'OpenCV image': A copy of the image passed but with a color channel removed
        """
        (B, G, R) = cv2.split(image)
        zeros = np.zeros(image.shape[:2], dtype="uint8")

        if image_channel == "green":
            return cv2.merge([B, zeros, R])
        elif image_channel == "blue":
            return cv2.merge([zeros, G, R])
        elif image_channel == "red":
            return cv2.merge([B, G, zeros])
        else:
            raise NameError('Invalid Colour Selection! Only red, green, blue are valid colour selections')

    def blackHat(self, image, rect_kernel_size=(13, 7)):
        """
        This function applies blackhat color changes to the image passed
        Author(s):
            Stephan Nell
        Args:
            image (:obj:'OpenCV image'): Image to which black hat color changes should be
                applied to
            Integer list: Represent the kernel dimension by which blackHat morphology
                changes should be applied to.
        Returns:
            obj:'OpenCV image': A modified copy of the image where blackHat morphology was
                applied to an image.
        Todo:
            Add additional checks for invalid kernel sizes
        """
        rectangle_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, rect_kernel_size)
        return cv2.morphologyEx(image.copy(), cv2.MORPH_BLACKHAT, rectangle_kernel)

    def topHat(self, image, rect_kernel_size=(13, 7)):
        """
        This function applies tophat color changes to the image passed
        Author(s):
            Stephan Nell
        Args:
            image (:obj:'OpenCV image'): Image to which top hat color changes should be
                applied to.
            Integer list: Represent the kernel dimension by which topHat  morphology
                changes should be applied to.
        Returns:
                applied to an image.
        Todo:
            Add additional checks for invalid kernel sizes
        """
        rectangle_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, rect_kernel_size)
        return cv2.morphologyEx(image, cv2.MORPH_TOPHAT, rectangle_kernel)
