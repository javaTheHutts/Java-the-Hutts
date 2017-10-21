"""
Wraps all the functionality required for applying blurring techniques to an image.
"""

import cv2

__authors__ = "Stephan Nell, Nicolai van Niekerk"
__copyright__ = "Copyright 2017, Java the Hutts"
__license__ = "BSD"
__maintainer__ = "Stephan Nell"
__email__ = "nellstephanj@gmail.com"
__status__ = "Development"


class BlurManager:
    """
    The blur is responsible for applying different blur techniques to the images passed.
    """
    def __init__(self, blur_type, kernel_size):
        """
        Initialise Blur Manager.

        :param blur_type (str): Indicates the type of blur operation that should be applied to the image.
        :param kernel_size (int tuple): Indicates the kernel size for blurring operations.

        Raises:
            - TypeError: If a none string value is passed for blur_type.

        """
        if not isinstance(blur_type, str):
            raise TypeError(
                'Bad type for arg blur_type - expected string. Received type "%s".' %
                type(blur_type).__name__
            )

        self.blur_type = blur_type
        self.kernel_size = kernel_size

    def apply(self, image):
        """
        This performs the blurring.

        :param image: The image to be blurred.

        Raises:
            - NameError: If invalid blur type is provided i.e. Normal, Gaussian or Median.

        Returns:
            - (obj): The blurred OpenCV image.

        """
        if self.blur_type == "gaussian":
            return self.gaussianBlur(image, self.kernel_size)
        elif self.blur_type == "normal":
            return self.blur(image, self.kernel_size)
        elif self.blur_type == "median":
            return self.medianBlur(image, self.kernel_size)
        else:
            raise NameError('Invalid Blur Selection! Try "normal", "gaussian" or "median" thresholding types.')

    def blur(self, image, blur_kernel=[(3, 3)]):
        """
        This function applies basic blurring to the image passed.

        :param image (obj): OpenCV image to which basic blurring should be applied to.
        :param blur_kernel (int list): Represent the kernel dimension by which basic blurring should be applied to.

        Raises:
            - ValueError: If a blur_kernel with an invalid length is provided.
            - TypeError: If a blur_kernel is not of type list.

        Returns:
            - (obj): A modified copy of the OpenCV image where basic blurring was applied to the image.

        """
        if not (isinstance(blur_kernel, list)):
            raise TypeError('Invalid kernel type provided for normal blurring. Blur kernel supports list type')
        if not len(blur_kernel[0]) == 2:
            raise ValueError('Invalid kernel size - blur_kernel list can only contain 2 items.')
        for (kX, kY) in blur_kernel:
            blurred = cv2.blur(image, (kX, kY))
        return blurred

    def gaussianBlur(self, image, blur_kernel=[(7, 7)]):
        """
        This function applies Gaussian blurring to the image passed.

        :param image (obj): OpenCV image to which Gaussian blurring should be applied to.
        :param blur_kernel (Integer list): Represent the kernel dimension by which basic blurring
                should be applied to.

        Raises:
            - ValueError: If a blur_kernel with an invalid length is provided.
            - TypeError: If a blur_kernel is not of type list.

        Returns:
            - (obj): A modified copy of the OpenCV image where Gaussian blurring was applied to the image.
        """
        if not (isinstance(blur_kernel, list)):
            raise TypeError('Invalid kernel type provided for gaussian blur. Blur kernel supports list type.')
        if not len(blur_kernel[0]) == 2:
            raise ValueError('Invalid kernel size - blur_kernel list can only contain 2 items.')
        for (kX, kY) in blur_kernel:
            blurred = cv2.GaussianBlur(image, (kX, kY), 0)
        return blurred

    def medianBlur(self, image, blur_kernel=[3]):
        """
        This function applies Median blurring to the image passed.

        :param image (obj): OpenCV image to which Median blurring should be applied to.
        :param blur_kernel (int list): Represent the kernel dimension by which median blurring should be applied to.

        Raises:
            - TypeError: If  a blur_kernel is not of type list.
            - ValueError: If a blur_kernel with an invalid length is provided.

        Returns:
            (obj): A modified copy of the image where Median blurring was applied to the image.

        """
        if not (isinstance(blur_kernel[0], int)):
            raise TypeError('Invalid kernel type provided for median blur. Blur kernel supports list type')
        if not len(blur_kernel) == 1:
            raise ValueError('Invalid kernel size only one integer value should be provided')
        for k in blur_kernel:
            blurred = cv2.medianBlur(image, k)
        return blurred
