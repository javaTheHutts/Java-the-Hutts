from processing import FaceDetector
import argparse
import imutils
import cv2
import os

FACE_DETECTOR_PATH = "{base_path}/cascades/haarcascade_frontalface_default.xml".format(
    base_path=os.path.abspath(os.path.dirname(__file__)))

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
                help="path to input image for profile extraction")
args = vars(ap.parse_args())

fd = FaceDetector(FACE_DETECTOR_PATH)
image = cv2.imread(args["image"])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
(face, _) = fd.removeFace(gray)
cv2.imwrite("output/face.png", face)
