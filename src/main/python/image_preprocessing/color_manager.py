import cv2
import numpy as np


class ColorManager:
    """
    The Color manager is responsible for applying several color management techniques
    to the image passed.
    """
    def __init__(self, color_extraction_type, channel="green", kernel_size=(13, 7)):
        """
        Initialise Color Manager.
        Authors(s):
            Nicolai van Niekerk, Stephan Nell
        Args:
            color_extraction_type (str): Indicates the type of color extraction that
                should be applied.
            channel (str): Indicates the color channel that should be extracted.
                Only red, green and blue (RGB) are considered valid colors to extracts.
            kernel_size (integer tuple): Indicates the kernel size for operation that
                require modification of the kernel size, like black and white-hat modifications.
        Returns:
            None

        """
        self.color_extraction_type = color_extraction_type
        self.channel = channel
        self.kernel_size = kernel_size

    def apply(self, image):
        """
        This performs the specified processing technique.
        Author(s):
            Nicolai van Niekerk, Stephan Nell
        Args:
            image: The image to which the technique must be applied.
        Raises:
            NameError: If invalid color extraction type is provided i.e.
                histogram, extract, black hat or top hat (white hat).
        Returns:
            obj:'OpenCV image': The modified image

        """
        if self.color_extraction_type == "extract":
            return self.extractChannel(image, self.channel)
        elif self.color_extraction_type == "histogram":
            return self.histEqualisation(image)
        elif self.color_extraction_type == "blackHat":
            return self.blackHat(image, self.kernel_size)
        elif self.color_extraction_type == "topHat":
            return self.topHat(image, self.kernel_size)
        elif self.color_extraction_type == "whiteHat":
            return self.topHat(image, self.kernel_size)
        else:
            raise NameError('Invalid Color extraction type! \n'
                            'Try: "histrogram", "extract", "blackhat", "topHat" or "whiteHat"')

    @staticmethod
    def histEqualisation(image):
        """
        This function applies histogram equalisation to the image passed.
        Author(s):
            Stephan Nell
        Args:
            image (:obj:'OpenCV image'): Image to which histogram equalisation should be applied to.
        Returns:
            obj:'OpenCV image': The Histogram equalised image.
        """
        image_grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return cv2.equalizeHist(image_grey)

    def extractChannel(self, image, image_channel="green"):
        """
        This function extracts a selected color channel from an image.
        Author(s):
            Stephan Nell
        Args:
            image (:obj:'OpenCV image'): Image to which image channel should be removed.
            str: Color that should be removed valid color red, green, blue.
        Raises:
            NameError: If invalid colour is selected i.e. not red, green, blue
        Returns:
            obj:'OpenCV image': A copy of the image passed but with a color channel removed.

        """
        (B, G, R) = cv2.split(image)
        zeros = np.zeros(image.shape[:2], dtype="uint8")

        if image_channel == "green":
            return cv2.merge([B, zeros, R])
        elif image_channel == "blue":
            return cv2.merge([zeros, G, R])
        elif image_channel == "red":
            return cv2.merge([B, G, zeros])
        elif image_channel == "red_blue":
            return cv2.merge([zeros, G, zeros])
        elif image_channel == "green_blue":
            return cv2.merge([zeros, zeros, R])
        elif image_channel == "green_red":
            return cv2.merge([B, zeros, zeros])
        else:
            raise NameError('Invalid Colour Selection! Only red, green, blue are valid colour selections')

    def blackHat(self, image, rect_kernel_size=(13, 7)):
        """
        This function applies blackhat color changes to the image passed.
        Author(s):
            Stephan Nell
        Args:
            image (:obj:'OpenCV image'): Image to which black hat color changes should be
                applied to
            rect_kernel_size (list): Represent the kernel dimension by which blackHat morphology
                changes should be applied to.
        Raises:
            TypeError: If the kernel size type is not a tuple.
            ValueError: If the kernel size tuple contains more than 2 items.
        Returns:
            obj:'OpenCV image': A modified copy of the image where blackHat morphology was
                applied to an image.

        """
        if not (isinstance(rect_kernel_size, tuple)):
            raise TypeError('Invalid kernel type provided. Black hat kernel Supports tuple type')
        if not len(rect_kernel_size) == 2:
            raise ValueError('Invalid kernel size - rect_kernel_size list can only contain 2 items.')
        rectangle_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, rect_kernel_size)
        return cv2.morphologyEx(image.copy(), cv2.MORPH_BLACKHAT, rectangle_kernel)

    def topHat(self, image, rect_kernel_size=(13, 7)):
        """
        This function applies tophat color changes to the image passed.
        Author(s):
            Stephan Nell
        Args:
            image (:obj:'OpenCV image'): Image to which top hat color changes should be
                applied to.
            rect_kernel_size (list): Represents the kernel dimension by which topHat  morphology
                changes should be applied to.
        Raises:
            TypeError: If the kernel size type is not a tuple.
            ValueError: If the kernel size tuple contains more than 2 items.
        Returns:
                obj:'OpenCV image': A modified copy of the image where topHat morphology was
                applied to an image.
        """
        if not (isinstance(rect_kernel_size, tuple)):
            raise TypeError('Invalid kernel type provided. Top hat Kernel supports tuple type')
        if not len(rect_kernel_size) == 2:
            raise ValueError('Invalid kernel Size - rect_kernel_size list can only contain 2 items.')
        rectangle_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, rect_kernel_size)
        return cv2.morphologyEx(image, cv2.MORPH_TOPHAT, rectangle_kernel)
