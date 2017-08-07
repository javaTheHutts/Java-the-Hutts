"""
----------------------------------------------------------------------
Author(s): Stephan Nell, Jan-Justin van Tonder
----------------------------------------------------------------------
Driver for extracting text from the image passed and converting
extracted text into a JSON object
----------------------------------------------------------------------
Example:
   python text_extract.py --image img/ID2.jpeg --color "red" --thresholding "otsu" --blur "median" --kernel 3 3
   python text_extract.py  --image img/idcard.jpg --color "green" --thresholding "adaptive" --blur "median"
----------------------------------------------------------------------
"""

from PIL import Image
from prototype.preprocessing.thresholding_manager import ThresholdingManager
from prototype.preprocessing.blur_manager import BlurManager
from prototype.preprocessing.color_manager import ColorManager
from prototype.preprocessing.simplification_manager import SimplificationManager
from prototype.processing.face_manager import FaceDetector
from prototype.processing.barcode_manager import BarCodeManager
from prototype.processing.text_manager import TextManager

import pytesseract
import cv2
import os

# Constants path to trained data for Shape Predictor.
SHAPE_PREDICTOR_PATH = "{base_path}/trained_data/shape_predictor_face_landmarks.dat".format(
    base_path=os.path.abspath(os.path.dirname(__file__)))

DESKTOP = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')


class TextExtractor:
    def extract(self, img, thresh="adaptive", blurr="median", clr="red", rm=False, knl=[9]):

        image = img

        simplification_manager = SimplificationManager()
        barcode_manager = BarCodeManager()
        color_manager = ColorManager()
        face_detector = FaceDetector(SHAPE_PREDICTOR_PATH)
        image = simplification_manager.perspectiveTransformation(image)
        cv2.imwrite(DESKTOP + "/output/3.png", image)
        data = {}
        barcode_data_found, barcode_scan_data, image = barcode_manager.get_barcode_info(image)
        if barcode_data_found:
            data = {
                'identity_number': barcode_scan_data.decode('utf-8'),
            }

        if rm:
            image = face_detector.blur_face(image)
            cv2.imwrite(DESKTOP + "/output/4.png", image)

        if knl:
            if blurr == "median":
                blur_kernel = [9]
            else:
                blur_kernel = [(9, 9)]
        else:
            blur_kernel = knl

        if blurr is not None:
            blur_manager = BlurManager()
            if blurr == "blur":
                image = blur_manager.blur(image, blur_kernel=blur_kernel)
            elif blurr == "gaussian":
                image = blur_manager.gaussianBlur(image, blur_kernel=blur_kernel)
            elif blurr == "median":
                image = blur_manager.medianBlur(image, blur_kernel=blur_kernel)
            cv2.imwrite(DESKTOP + "/output/5.png", image)

        if clr is not None:
            if clr == "blackhat":
                image = color_manager.blackHat(image)
            elif clr == "tophat":
                image = color_manager.topHat(image)
            else:
                image = color_manager.extractChannel(image, clr)
            cv2.imwrite(DESKTOP + "/output/6.png", image)

        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        cv2.imwrite(DESKTOP + "/output/7.png", image)

        if thresh is not None:
            thresh_manager = ThresholdingManager()
            if thresh == "adaptive":
                image = thresh_manager.adaptiveThresholding(image)
            elif thresh == "otsu":
                image = thresh_manager.otsuThresholding(image)

        filename = "{}.png".format(os.getpid())
        cv2.imwrite(filename, image)

        cv2.imwrite(DESKTOP+"/output/8.png", image)
        text = pytesseract.image_to_string(Image.open(filename))
        os.remove(filename)

        # Text cleanup and retrieval
        text_manager = TextManager()
        print(text, "\n------------------------------------------------------")
        clean_text = text_manager.clean_up(text)
        print(clean_text, "\n -----------------------------------------------")
        id_details = text_manager.dictify(clean_text, data)
        print(id_details)
        return id_details
