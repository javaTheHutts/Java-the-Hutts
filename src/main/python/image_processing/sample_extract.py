from image_processing.build_director import BuildDirector
from extraction.text_manager import TextManager
from extraction.simplification_manager import SimplificationManager
from extraction.barcode_manager import BarCodeManager
import pytesseract
from PIL import Image
import cv2
import os

DESKTOP = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')


class TextExtractor:
    """
        The TextExtractor extracts text from the ID image
    """
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
        simplification_manager = SimplificationManager()
        barcode_manager = BarCodeManager()
        data = {}

        # Perform perspective transformation and read from barcode
        image = simplification_manager.perspectiveTransformation(img)
        cv2.imwrite(DESKTOP + "/output/3.png", image)
        barcode_data_found, barcode_scan_data, barcoded_image = barcode_manager.get_barcode_info(image)
        if barcode_data_found:
            data = {
                'identity_number': barcode_scan_data.decode('utf-8'),
            }

        # Process image
        pipeline = BuildDirector.construct()
        image = pipeline.process(barcoded_image)

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
