# python text_extract.py --image img/ID.jpg  --thresholding "adaptive" --blur "blur"
# python text_extract.py --image img/ID2.jpeg --color "green"
# --thresholding "otsu" --blur "median" --kernel 3 3


from PIL import Image
from preprocessing import ThresholdingManager
from preprocessing import BlurManager
from preprocessing import ColorManager
import pytesseract
import argparse
import cv2
import os

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
                help="path to input image to be OCR'd")
ap.add_argument("-t", "--thresholding", type=str, default=None,
                help="type of thresholding technique")
ap.add_argument("-b", "--blur", type=str, default="gaussian",
                help="Remove color channel")
ap.add_argument("-c", "--color", type=str, default=None,
                help="Remove color channel")
ap.add_argument("-k", "--kernel", default=None, nargs='+', type=int, help="Kernel size for selected blur")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])
color_manager = ColorManager(image)
if args["color"] is not None:
    image = color_manager.extractChannel(image, args["color"])
if args["kernel"] is not None:
    blur_kernel = args["kernel"]
else:
    if args["blur"] == "median":
        blur_kernel = [3]
    else:
        blur_kernel = [(3, 3)]

image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# image = color_manager.histEqualisation(image)


if args["blur"] is not None:
    blur_manager = BlurManager(image)
    if args["blur"] == "blur":
        image = blur_manager.blur(image, blur_kernel=blur_kernel)
    elif args["blur"] == "gaussian":
        image = blur_manager.gaussianBlur(image, blur_kernel=blur_kernel)
    elif args["blur"] == "median":
        image = blur_manager.medianBlur(image, blur_kernel=blur_kernel)

if args["thresholding"] is not None:
    thresh_manager = ThresholdingManager(image)
    if args["thresholding"] == "adaptive":
        image = thresh_manager.adaptiveThresholding(image)
    elif args["thresholding"] == "otsu":
        image = thresh_manager.otsuThresholding(image)

filename = "{}.png".format(os.getpid())
cv2.imwrite(filename, image)

text = pytesseract.image_to_string(Image.open(filename))
os.remove(filename)
print(text)

cv2.imwrite("output/img.png", image)
