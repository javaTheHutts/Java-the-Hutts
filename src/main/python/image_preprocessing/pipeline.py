import cv2
import os
from hutts_utils.hutts_logger import logger
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

    def process_text_extraction(self, image, remove_face=False):
        """
        This function applies all the processing needed to extract text from a image.
        Author(s):
            Nicolai van Niekerk
        Args:
            image (:obj:'OpenCV image'): Image to which processing should be applied to.
            remove_face :boolean: If the remove face flag is set to true extra processes will
                be activated during the pre-processing phase to remove the face from the image.
        Returns:
            image: The processed image.

        """
        # Remove face from image.
        logger.info("Removing face: " + str(remove_face))
        if remove_face:
            logger.info("REMOVING FACE...")
            image = self.face_detector.blur_face(image)
            cv2.imwrite(DESKTOP + "/output/4.png", image)

        # Blur image.
        logger.info("Blurring image...")
        blur_image = self.blur_manager.apply(image)
        cv2.imwrite(DESKTOP + "/output/5.png", blur_image)

        # Apply channel image_processing, tophat, blackhat or histogram equalization.
        logger.info("Removing color channel...")
        color_image = self.color_manager.apply(blur_image)
        cv2.imwrite(DESKTOP + "/output/6.png", color_image)

        # Convert image to grayscale.
        logger.info("Converting image to grayscale...")
        gray_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2GRAY)
        cv2.imwrite(DESKTOP + "/output/7.png", gray_image)

        # Apply thresholding.
        logger.info("Applying thresholding...")
        thresholded_image = self.threshold_manager.apply(gray_image)
        cv2.imwrite(DESKTOP + "/output/8.png", thresholded_image)

        return thresholded_image

    def process_face_extraction(self, image):
        """
        This function applies all the processing needed to extract a face from a image.
        Author(s):
            Stephan Nell
        Args:
            image (:obj:'OpenCV image'): Image to which processing should be applied to.
        Returns:
            image: The processed image.

        """
        logger.info("Extracting face from image")
        (extracted_face, _) = self.face_detector.extract_face(image)

        return extracted_face
