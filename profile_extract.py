from processing import FaceDetector
from preprocessing import SimplificationManager
import argparse
import cv2
import os

SHAPE_PREDICTOR_PATH = "{base_path}/trained_data/shape_predictor_face_landmarks.dat".format(
    base_path=os.path.abspath(os.path.dirname(__file__)))

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
                help="path to input image for profile extraction")
args = vars(ap.parse_args())


face_detector = FaceDetector(SHAPE_PREDICTOR_PATH)
image = cv2.imread(args["image"])
simplification_manager = SimplificationManager(image)
image = simplification_manager.perspectiveTransformation(image)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
(face, image) = face_detector.extractFace(gray)
cv2.imshow("Face",face)
cv2.imshow("Image", image)
cv2.waitKey(0)
cv2.imwrite("output/face.png", face)
cv2.imwrite("output/faceimage.png", image)
