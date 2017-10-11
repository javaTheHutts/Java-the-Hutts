import cv2


class BlurManager:
    """
    The blur is responsible for applying different blur techniques to the images passed.
    """
    def __init__(self, blur_type, kernel_size):
        """
        Initialise Blur Manager.
        Authors(s):
            Nicolai van Niekerk, Stephan Nell
        Args:
            blur_type (str): Indicates the type of blur operation that should be applied to the image.
            kernel_size (integer tuple): Indicates the kernel size for blurring operations.
        Raises:
            TypeError: If a none string value is passed for blur_type
        Returns:
            None

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
        Author(s):
            Nicolai van Niekerk, Stephan Nell
        Args:
            image: The image to be blurred.
        Raises:
            NameError: If invalid blur type is provided i.e. Normal, Gaussian or Median.
        Returns:
            obj:'OpenCV image': The blurred image.

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
        Author(s):
            Stephan Nell
        Args:
            image (:obj:'OpenCV image'): Image to which basic blurring should be applied to.
            blur_kernel (Integer list): Represent the kernel dimension by which basic blurring should be applied to.
            Integer list: Represent the kernel dimension by which basic blurring should be applied to.
        Raises:
            ValueError: If a blur_kernel with an invalid length is provided.
            TypeError: If  a blur_kernel is not of type list.
        Returns:
            obj:'OpenCV image': A modified copy of the image where basic blurring was applied to the image.
        """
        if not (isinstance(blur_kernel, list)):
            raise TypeError('Invalid Kernel type Provided for normal blurring. Blur Kernel Supports list type')
        if not len(blur_kernel[0]) == 2:
            raise ValueError('Invalid Kernel Size - blur_kernel list can only contain 2 items.')
        for (kX, kY) in blur_kernel:
            blurred = cv2.blur(image, (kX, kY))
        return blurred

    def gaussianBlur(self, image, blur_kernel=[(7, 7)]):
        """
        This function applies Gaussian blurring to the image passed.
        Author(s):
            Stephan Nell
        Args:
            image (:obj:'OpenCV image'): Image to which Gaussian blurring should be applied to.
            blur_kernel (Integer list): Represent the kernel dimension by which basic blurring should be applied to.
            Integer list: Represent the kernel dimension by which basic blurring should be applied to.
        Raises:
            ValueError: If a blur_kernel with an invalid length is provided.
            TypeError: If  a blur_kernel is not of type list.
        Returns:
            obj:'OpenCV image': A modified copy of the image where Gaussian blurring was applied to the image.
        """
        if not (isinstance(blur_kernel, list)):
            raise TypeError('Invalid Kernel type Provided for gaussian blur. Blur Kernel Supports list type')
        if not len(blur_kernel[0]) == 2:
            raise ValueError('Invalid Kernel Size - blur_kernel list can only contain 2 items.')
        for (kX, kY) in blur_kernel:
            blurred = cv2.GaussianBlur(image, (kX, kY), 0)
        return blurred

    def medianBlur(self, image, blur_kernel=[3]):
        """
        This function applies Median blurring to the image passed.
        Author(s):
            Stephan Nell
        Args:
            image (:obj:'OpenCV image'): Image to which Median blurring should be applied to.
            blur_kernel (Integer array): Represent the kernel dimension by which median blurring should be applied to.
            Integer array: Represent the kernel dimension by which median blurring should be applied to.
        Raises:
            TypeError: If  a blur_kernel is not of type list.
            ValueError: If a blur_kernel with an invalid length is provided.
        Returns:
            obj:'OpenCV image': A modified copy of the image where Median blurring was applied to the image.
        """
        if not (isinstance(blur_kernel[0], int)):
            raise TypeError('Invalid Kernel type Provided for median blur. Blur Kernel Supports list type')
        if not len(blur_kernel) == 1:
            raise ValueError('Invalid Kernel Size only one integer value should be provided')
        for k in blur_kernel:
            blurred = cv2.medianBlur(image, k)
        return blurred
