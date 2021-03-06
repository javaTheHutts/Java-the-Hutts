"""
This is an object that handles the entire process of extracting data from an image
from a high-level perspective.
"""

import cv2
import os
from hutts_verification.utils.hutts_logger import logger

__authors__ = "Nicolai van Niekerk, Stephan Nell"
__copyright__ = "Copyright 2017, Java the Hutts"
__license__ = "BSD"
__maintainer__ = "Nicolai van Niekerk"
__email__ = "nicvaniek@gmail.com"
__status__ = "Development"

DESKTOP = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')


class Pipeline:
    """
    The Pipeline will perform all necessary processing on the image and is built by the PipelineBuilder.

    :param blur_manager (BlurManager): The BlurManager that is used in this pipeline.
    :param color_manager (ColorManager): The ColorManager that is used in this pipeline.
    :param face_detector (FaceDetector): The FaceDetector that is used in this pipeline.
    :param threshold_manager (ThresholdManager): The ThresholdManager that is used in this pipeline.

    """
    def __init__(self, blur_manager=None, color_manager=None, face_detector=None, threshold_manager=None):
        """
        Initialize Pipeline with parameters passed from t￼￼￼￼￼￼he Builder.

        :param blur_manager (BlurManager): The BlurManager.
        :param color_manager (ColorManager): The ColorManager.
        :param face_detector (FaceDetector): The FaceDetector.
        :param threshold_manager (ThresholdManager): The ThresholdManager.

        """
        self.blur_manager = blur_manager
        self.color_manager = color_manager
        self.face_detector = face_detector
        self.threshold_manager = threshold_manager

    def process_text_extraction(self, useIO, image, remove_face=False):
        """
        This function applies all the processing needed to extract text from a image.

        :param useIO (boolean): Whether or not to write images to disk.
        :param image (obj): Image that should be processed.
        :param remove_face (boolean): If the remove face flag is set to true, extra processes will
                be activated during the pre-processing phase to remove the face from the image.

        Returns:
            - (obj): The processed image.

        """

        # Remove face from image.
        if remove_face:
            logger.info("Removing face: " + str(remove_face))
            image = self.face_detector.blur_face(image)
            if useIO:
                cv2.imwrite(DESKTOP + "/output/4.png", image)

        # Blur image.
        logger.info("Blurring image...")
        blur_image = self.blur_manager.apply(image)
        if useIO:
            cv2.imwrite(DESKTOP + "/output/5.png", blur_image)

        # Apply channel image_processing, tophat, blackhat or histogram equalization.
        logger.info("Removing color channel...")
        color_image = self.color_manager.apply(blur_image)
        if useIO:
            cv2.imwrite(DESKTOP + "/output/6.png", color_image)

        # Convert image to grayscale.
        logger.info("Converting image to grayscale...")
        gray_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2GRAY)
        if useIO:
            cv2.imwrite(DESKTOP + "/output/7.png", gray_image)

        # Apply thresholding.
        logger.info("Applying thresholding...")
        thresholded_image = self.threshold_manager.apply(gray_image)
        if useIO:
            cv2.imwrite(DESKTOP + "/output/8.png", thresholded_image)

        return thresholded_image

    def process_face_extraction(self, image):
        """
        This function applies all the processing needed to extract a face from a image.

        :param image (obj): Image to which processing should be applied to.

        Returns:
            - (obj): The processed image.

        """
        logger.info("Extracting face from image")
        extracted_face = self.face_detector.extract_face(image)

        return extracted_face
