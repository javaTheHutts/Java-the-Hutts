# python text_extract.py --image img/ID.jpg  --thresholding "adaptive" --blur "blur"
# python text_extract.py --image img/ID2.jpeg --color "green"
# --thresholding "otsu" --blur "median" --kernel 3 3
# python text_extract.py --color "blackhat" --image img/ID2.jpeg
# python text_extract.py  --image img/idcard.jpg --color "green" --thresholding "adaptive" --blur "median"



from PIL import Image
from preprocessing import ThresholdingManager
from preprocessing import BlurManager
from preprocessing import ColorManager
from preprocessing import SimplificationManager
from processing import FaceDetector
import pytesseract
import argparse
import cv2
import os

SHAPE_PREDICTOR_PATH = "{base_path}/trained_data/shape_predictor_face_landmarks.dat".format(
    base_path=os.path.abspath(os.path.dirname(__file__)))

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
                help="path to input image to be OCR'd")
ap.add_argument("-t", "--thresholding", type=str, default=None,
                help="type of thresholding technique")
ap.add_argument("-b", "--blur", type=str, default="gaussian",
                help="Blur image")
ap.add_argument("-c", "--color", type=str, default=None,
                help="Remove color channel")
ap.add_argument("-r", "--remove", type=bool, default=None,
                help="Remove Face")
ap.add_argument("-k", "--kernel", default=None, nargs='+', type=int, help="Kernel size for selected blur")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])

simplification_manager = SimplificationManager(image)
image = simplification_manager.perspectiveTransformation(image)
cv2.imwrite("output/warped.png", image)
color_manager = ColorManager(image)
face_detector = FaceDetector(SHAPE_PREDICTOR_PATH)

if args["color"] is not None:
    if args["color"] == "blackhat":
        image = color_manager.blackHat(image)
    elif args["color"] == "tophat":
        image = color_manager.topHat(image)
    else:
        image = color_manager.extractChannel(image, args["color"])
    cv2.imwrite("output/colour_extract.png", image)

if args["kernel"] is not None:
    blur_kernel = args["kernel"]
else:
    if args["blur"] == "median":
        blur_kernel = [3]
    else:
        blur_kernel = [(3, 3)]

image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imwrite("output/gray.png", image)

if args["remove"] is True:
    (_, image) = face_detector.extractFace(image)


if args["blur"] is not None:
    blur_manager = BlurManager(image)
    if args["blur"] == "blur":
        image = blur_manager.blur(image, blur_kernel=blur_kernel)
    elif args["blur"] == "gaussian":
        image = blur_manager.gaussianBlur(image, blur_kernel=blur_kernel)
    elif args["blur"] == "median":
        image = blur_manager.medianBlur(image, blur_kernel=blur_kernel)

cv2.imwrite("output/blur.png", image)
if args["thresholding"] is not None:
    thresh_manager = ThresholdingManager(image)
    if args["thresholding"] == "adaptive":
        image = thresh_manager.adaptiveThresholding(image)
    elif args["thresholding"] == "otsu":
        image = thresh_manager.otsuThresholding(image)

cv2.imwrite("output/thresh.png", image)
filename = "{}.png".format(os.getpid())
cv2.imwrite(filename, image)

cv2.imwrite("output/Extraction.png", image)
cv2.imshow("show", image)
text = pytesseract.image_to_string(Image.open(filename))
os.remove(filename)
print(text)
cv2.waitKey(0)