import cv2
import os

class Pipeline:
    """
    The Pipeline will perform all necessary processing on the image and is built by the PipelineBuilder
    """
    def __init__(self, blur_manager=None, color_manager=None, face_detector=None, threshold_manager=None):
        """
        Initialize Pipeline with parameters passed from the Builder
        """
        self.blur_manager = blur_manager
        self.color_manager = color_manager
        self.face_detector = face_detector
        self.threshold_manager = threshold_manager

    def process(self, image, rm=False):
        """
        This function applies all the processing needed on the image
        Author(s):
            Stephan Nell, Nicolai van Niekerk
        Args:
            image (:obj:'OpenCV image'): Image to which processing should be applied to.
        Returns:
            image: The processed image
        Todo:

        """
        # Remove face from image
        if rm:
            image = self.face_detector.blur_face(image)

        # Blur image
        image = self.blur_manager.apply(image)

        # Apply channel extraction, tophat, blackhat or histogram equalization
        image = self.color_manager.apply(image)

        # Convert image to grayscale
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Apply thresholding
        image = self.threshold_manager.apply(image)

        return image
