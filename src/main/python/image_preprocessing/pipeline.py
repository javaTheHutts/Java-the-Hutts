import cv2
import os
DESKTOP = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')


class Pipeline:
    """
    The Pipeline will perform all necessary processing on the image and is built by the PipelineBuilder.
    """
    def __init__(self, blur_manager=None, color_manager=None, face_detector=None, threshold_manager=None):
        """
        Initialize Pipeline with parameters passed from the Builder.
        """
        self.blur_manager = blur_manager
        self.color_manager = color_manager
        self.face_detector = face_detector
        self.threshold_manager = threshold_manager

    def process(self, image, remove_face=False):
        """
        This function applies all the processing needed on the image.
        Author(s):
            Nicolai van Niekerk
        Args:
            image (:obj:'OpenCV image'): Image to which processing should be applied to.
            remove_face boolean: If the remove face flag is set to true extra processes will
                be activated during the pre-processing phase to remove the face from the image.
        Returns:
            image: The processed image.

        """
        # Remove face from image.
        if remove_face:
            image = self.face_detector.blur_face(image)
            cv2.imwrite(DESKTOP + "/output/4.png", image)

        # Blur image.
        blur_image = self.blur_manager.apply(image)
        cv2.imwrite(DESKTOP + "/output/5.png", blur_image)

        # Apply channel image_processing, tophat, blackhat or histogram equalization.
        color_image = self.color_manager.apply(blur_image)
        cv2.imwrite(DESKTOP + "/output/6.png", color_image)

        # Convert image to grayscale.
        gray_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2GRAY)
        cv2.imwrite(DESKTOP + "/output/7.png", gray_image)

        # Apply thresholding.
        thresholded_image = self.threshold_manager.apply(gray_image)
        cv2.imwrite(DESKTOP + "/output/8.png", thresholded_image)

        return thresholded_image
