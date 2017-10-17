"""
This class wraps all the functionality required to extract text from an image.
"""

import os
import cv2
import pytesseract
from PIL import Image
from hutts_verification.image_preprocessing.build_director import BuildDirector
from hutts_verification.image_processing.text_cleaner import TextCleaner
from hutts_verification.image_processing.simplification_manager import SimplificationManager
from hutts_verification.image_processing.barcode_manager import BarCodeManager
from hutts_verification.image_preprocessing.template_matching import TemplateMatching
from hutts_verification.image_processing.context_manager import ContextManager
from hutts_verification.utils.hutts_logger import logger, prettify_json_message

__author__ = "Nicolai van Niekerk"
__copyright__ = "Copyright 2017, Java the Hutts"
__license__ = "BSD"
__maintainer__ = "Nicolai van Niekerk"
__email__ = "nicvaniek@gmail.com"
__status__ = "Development"

DESKTOP = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')


class TextExtractor:
    """
    The TextExtractor extracts text from the ID image.
    """

    def __init__(self, preferences):
        """
        Initialise Text Extractor.

        :param preferences (dict): User-specified CV techniques.

        """
        self.preferences = preferences
        self.remove_face = 'false'
        self._context_manager = ContextManager()
        self._text_cleaner = TextCleaner()

    def extract(self, img):
        """
        This function is a sample that demonstrates how text would be extracted.

        :param img (obj): The image of the ID that contains the text to be extracted.

        Returns:
            - id_details (obj): The extracted information.

        """
        if 'remove_face' in self.preferences:
            self.remove_face = self.preferences['remove_face'] == 'true'
        logger.debug('self.remove_face: ' + str(self.remove_face))

        simplification_manager = SimplificationManager()
        barcode_manager = BarCodeManager()
        data = {}

        # Perform perspective transformation and read from barcode.
        logger.info('Performing perspective transformation...')
        image = simplification_manager.perspectiveTransformation(img, self.preferences['useIO'])
        if self.preferences['useIO']:
            cv2.imwrite(DESKTOP + "/output/3.png", image)
        barcode_data_found, barcode_scan_data, barcoded_image = barcode_manager.get_barcode_info(image)
        if barcode_data_found:
            logger.info('Barcode successfully scanned')
            data = {
                'identity_number': barcode_scan_data.decode('utf-8'),
            }

        # Process image
        if 'id_type' in self.preferences:
            identification_type = self.preferences['id_type']
            logger.info("No template matching required")
            logger.info("Identification type: " + identification_type)
        else:
            template_match = TemplateMatching()
            logger.info('Performing template matching...')
            identification_type = template_match.identify(barcoded_image)

        logger.info('Constructing text extraction pipeline')
        pipeline = BuildDirector.construct_text_extract_pipeline(self.preferences, identification_type)
        image = pipeline.process_text_extraction(self.preferences['useIO'], barcoded_image, self.remove_face)

        # Extract and return text
        filename = "{}.png".format(os.getpid())
        cv2.imwrite(filename, image)

        text = pytesseract.image_to_string(Image.open(filename))
        os.remove(filename)

        # Log the uncleaned string to terminal.
        # This is for demonstration purposes.
        logger.debug('-' * 50)
        logger.debug('String to clean:')
        logger.debug('-' * 50)
        [logger.debug(log_line) for log_line in text.split('\n')]
        logger.debug('-' * 50)
        logger.info('Cleaning up text...')
        # Clean the OCR output text.
        clean_text = self._text_cleaner.clean_up(text)
        # Log the cleaned string to terminal.
        # This is for demonstration purposes.
        logger.debug('-' * 50)
        logger.debug('Cleaned text:')
        logger.debug('-' * 50)
        [logger.debug(log_line) for log_line in clean_text.split('\n')]
        logger.debug('-' * 50)
        # Get ID information from cleaned text.
        logger.info('Placing extracted text in a dictionary...')
        id_context = self._context_manager.get_id_context(identification_type)
        # Check if context was found.
        if id_context is None:
            # Log the error and raise it for handling.
            logger.error('Could not find ID context for ID type "%s"' % identification_type)
            raise ValueError('Could not identify ID type')
        id_details = id_context.get_id_info(clean_text, barcode_data=data)
        # Log the retrieved ID information extracted text to terminal.
        # This is for demonstration purposes.
        logger.debug('-' * 50)
        logger.debug('Extracted ID details:')
        logger.debug('-' * 50)
        [logger.debug(id_details_line) for id_details_line in prettify_json_message(id_details).split('\n')]
        logger.debug('-' * 50)
        # Return the extracted ID information.
        return id_details


class FaceExtractor:
    """
    The FaceExtractor extracts the face region for the image passed.
    """
    def extract(self, img, use_io):
        """
        This function is a sample that demonstrates how the face would be extracted.

        :param img (obj): The image of the ID that contains the face that must be extracted.
        :param use_io (boolean): Whether or not images should be written to disk.

        Returns:
            - (obj): The extracted and aligned facial image.

        """
        simplification_manager = SimplificationManager()

        # Perform perspective transformation
        logger.info('Performing perspective transformation...')
        perspective_image = simplification_manager.perspectiveTransformation(img, use_io)
        if use_io:
            cv2.imwrite(DESKTOP + "/output/10.png", perspective_image)

        # Process image
        logger.info('Constructing facial extraction pipeline...')
        pipeline = BuildDirector.construct_face_extract_pipeline()
        image = pipeline.process_face_extraction(perspective_image)

        return image
