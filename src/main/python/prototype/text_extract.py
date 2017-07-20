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
from preprocessing import ThresholdingManager
from preprocessing import BlurManager
from preprocessing import ColorManager
from preprocessing import SimplificationManager
from processing import FaceDetector
from processing import BarCodeManager
from processing import TextManager

import pytesseract
import argparse
import cv2
import os
import json

# Constants path to trained data for Shape Predictor.
SHAPE_PREDICTOR_PATH = "{base_path}/trained_data/shape_predictor_face_landmarks.dat".format(
    base_path=os.path.abspath(os.path.dirname(__file__)))

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
                help="path to input image to be OCR'd")
ap.add_argument("-t", "--thresholding", type=str, default=None,
                help="type of thresholding technique")
ap.add_argument("-b", "--blur", type=str, default="gaussian",
                help="Blur image technique")
ap.add_argument("-c", "--color", type=str, default=None,
                help="Remove color channel")
ap.add_argument("-r", "--remove", type=bool, default=None,
                help="Remove Face")
ap.add_argument("-k", "--kernel", default=None, nargs='+', type=int,
                help="Kernel size for selected blur")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])

simplification_manager = SimplificationManager()
barcode_manager = BarCodeManager()
color_manager = ColorManager()
face_detector = FaceDetector(SHAPE_PREDICTOR_PATH)
image = simplification_manager.perspectiveTransformation(image)
cv2.imwrite("output/3-warped.png", image)


barcode_data_found, barcode_scan_data, image = barcode_manager.get_barcode_info(image)
if barcode_data_found:
    data = {
       'ID_number': barcode_scan_data.decode('utf-8'),
    }
    card_data = json.dumps(data)
    print(card_data)

if args["remove"] is True:
    image = face_detector.blur_face(image)
    cv2.imwrite("output/4-faceRemvoal.png", image)

if args["color"] is not None:
    if args["color"] == "blackhat":
        image = color_manager.blackHat(image)
    elif args["color"] == "tophat":
        image = color_manager.topHat(image)
    else:
        image = color_manager.extractChannel(image, args["color"])
    cv2.imwrite("output/5-colour_extract.png", image)

cv2.imwrite("output/colour_extract.png", image)
if args["kernel"] is not None:
    blur_kernel = args["kernel"]
else:
    if args["blur"] == "median":
        blur_kernel = [3]
    else:
        blur_kernel = [(3, 3)]

image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imwrite("output/6-gray.png", image)

if args["blur"] is not None:
    blur_manager = BlurManager()
    if args["blur"] == "blur":
        image = blur_manager.blur(image, blur_kernel=blur_kernel)
    elif args["blur"] == "gaussian":
        image = blur_manager.gaussianBlur(image, blur_kernel=blur_kernel)
    elif args["blur"] == "median":
        image = blur_manager.medianBlur(image, blur_kernel=blur_kernel)

cv2.imwrite("output/7-blur.png", image)
if args["thresholding"] is not None:
    thresh_manager = ThresholdingManager()
    if args["thresholding"] == "adaptive":
        image = thresh_manager.adaptiveThresholding(image)
    elif args["thresholding"] == "otsu":
        image = thresh_manager.otsuThresholding(image)

filename = "{}.png".format(os.getpid())
cv2.imwrite(filename, image)

cv2.imwrite("output/8-Extraction.png", image)
text = pytesseract.image_to_string(Image.open(filename))
os.remove(filename)

# Text cleanup and retrieval
text_manager = TextManager()
print(text, "\n------------------------------------------------------")
clean_text = text_manager.clean_up(text)
print(clean_text, "\n -----------------------------------------------")
id_details = text_manager.dictify(clean_text)
print(id_details)
