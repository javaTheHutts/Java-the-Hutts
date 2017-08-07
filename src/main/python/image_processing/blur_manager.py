import cv2


class BlurManager:
    """
    The blur is responsible for applying different blur techniques to the images passed
    """
    def __init__(self, type, kernel_size):
        """
        Initialise the Blur Manager
        """
        self.type = type
        self.kernel_size = kernel_size

        print("Initialise BlurManager")

    def apply(self, image):
        if self.type == "normal":
            return self.blur(image, self.kernel_size)
        elif self.type == "gaussian":
            return self.gaussianBlur(image, self.kernel_size)
        elif self.type == "median":
            return self.medianBlur(image, self.kernel_size)

    def blur(self, image, blur_kernel=[(3, 3)]):
        """
        This function applies basic blurring to the image passed.
        Author(s):
            Stephan Nell
        Args:
            image (:obj:'OpenCV image'): Image to which basic blurring should be applied to.
            Integer list: Represent the kernel dimension by which basic blurring should be applied to.
        Returns:
            obj:'OpenCV image': A modified copy of the image where basic blurring was applied to the image.
        Todo:
            Add additional checks for invalid kernel sizes
        """
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
            Integer list: Represent the kernel dimension by which basic blurring should be applied to.
        Returns:
            obj:'OpenCV image': A modified copy of the image where Gaussian blurring was applied to the image.
        Todo:
            Add additional checks for invalid kernel sizes
        """
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
            Integer array: Represent the kernel dimension by which median blurring should be applied to.
        Returns:
            obj:'OpenCV image': A modified copy of the image where Median blurring was applied to the image.
        Todo:
            Add additional checks for invalid kernel sizes
        """
        # To-Do Error Checking for different Kernel sizes
        for k in blur_kernel:
            blurred = cv2.medianBlur(image, k)
        return blurred
