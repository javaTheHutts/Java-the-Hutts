"""
----------------------------------------------------------------------
Author: Stephan Nell
----------------------------------------------------------------------
Driver for comparing two faces and determining if the two faces are the
same person or not.
----------------------------------------------------------------------
Example:
   python face_likeness.py --image1 img/ss.jpeg --image2 img/ssbook.jpg
   python face_likeness.py --image1 img/ID.jpg --image2 img/ssbook.jpg
   python face_likeness.py --image1 img/ss3.jpeg --image2 img/ssbook.jpg
----------------------------------------------------------------------
"""

from verification import FaceVerify
from processing import FaceDetector
import argparse
import cv2
import os

# Constants path to trained data for Shapre Predictor and Face recognition
SHAPE_PREDICTOR_PATH = "{base_path}/trained_data/shape_predictor_face_landmarks.dat".format(
    base_path=os.path.abspath(os.path.dirname(__file__)))

FACE_RECOGNITION_PATH = "{base_path}/trained_data/dlib_face_recognition_resnet_model_v1.dat".format(
    base_path=os.path.abspath(os.path.dirname(__file__)))

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-1", "--image1", required=True,
                help="Image 1 for comparison")
ap.add_argument("-2", "--image2", required=True,
                help="Image 2 for comparison")
args = vars(ap.parse_args())

image1 = cv2.imread(args["image1"])
image2 = cv2.imread(args["image2"])

face_detector = FaceDetector(SHAPE_PREDICTOR_PATH)
face_verify_manager = FaceVerify(SHAPE_PREDICTOR_PATH, FACE_RECOGNITION_PATH)

gray = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
(face1, _) = face_detector.extract_face(gray)

gray = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
(face2, _) = face_detector.extract_face(gray)

(face_match, face_threshold) = face_verify_manager.verify(face1, face2, 0.55)

if face_match:
    print("Face Matches with a percentage of:", (1-face_threshold) * 100, "%")
else:
    print("Face does not match with a threshold value of", (1 - face_threshold) * 100, "%")