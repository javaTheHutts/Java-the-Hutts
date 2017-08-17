from image_preprocessing.build_director import BuildDirector
from image_processing.text_manager import TextManager
from image_processing.simplification_manager import SimplificationManager
from image_processing.barcode_manager import BarCodeManager
from image_preprocessing.template_matching import TemplateMatching
import pytesseract
from PIL import Image
import cv2
import os

DESKTOP = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')


class TextExtractor:
    """
        The TextExtractor extracts text from the ID image
    """

    def __init__(self, preferences):
        """
        Initialise Text Extractor.
        Authors(s):
            Nicolai van Niekerk
        Args:
            preferences (dict): User-specified CV techniques.
        Returns:
            None

        """
        self.preferences = preferences

    def extract(self, img):
        """
        This function is a sample that demonstrates how text would be extracted
        Author(s):
            Nicolai van Niekerk
        Args:
            image: The image of the ID that contains the text tom be extracted
        Returns:
            id_details: JSON obj (The extracted information)
        Todo:
        """
        if 'remove_face' in self.preferences:
            remove_face = self.preferences['remove_face'] == 'true'
        else:
            remove_face = False

        simplification_manager = SimplificationManager()
        barcode_manager = BarCodeManager()
        data = {}

        # Perform perspective transformation and read from barcode.
        image = simplification_manager.perspectiveTransformation(img)
        cv2.imwrite(DESKTOP + "/output/3.png", image)
        barcode_data_found, barcode_scan_data, barcoded_image = barcode_manager.get_barcode_info(image)
        if barcode_data_found:
            data = {
                'identity_number': barcode_scan_data.decode('utf-8'),
            }

        # Process image
        template_match = TemplateMatching()
        identification_type = template_match.identify(barcoded_image)
        pipeline = BuildDirector.construct(self.preferences, identification_type)
        image = pipeline.process(barcoded_image, remove_face)

        # Extract and return text
        filename = "{}.png".format(os.getpid())
        cv2.imwrite(filename, image)

        text = pytesseract.image_to_string(Image.open(filename))
        os.remove(filename)

        text_manager = TextManager()
        print(text, "\n------------------------------------------------------")
        clean_text = text_manager.clean_up(text, ['_'])
        print(clean_text, "\n -----------------------------------------------")
        id_details = text_manager.dictify(clean_text, data)
        print(id_details)
        return id_details
