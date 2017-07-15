import cv2
from imutils.face_utils import FaceAligner
from imutils.face_utils import rect_to_bb
import dlib
import imutils

class FaceDetector:
    def __init__(self, shape_predictor_path):
        self.shape_predictor_path = shape_predictor_path

    def detect(self, image):
        # To Do if no face found return error
        detector = dlib.get_frontal_face_detector()
        rectangles = detector(image, 1)
        return rectangles[0]

    def extractFace(self, image):
        rectangle = self.detect(image)
        (x, y, w, h) = rect_to_bb(rectangle)
        predictor = dlib.shape_predictor(self.shape_predictor_path)
        face_aligner = FaceAligner(predictor, desiredFaceWidth=256)
        faceAligned = face_aligner.align(image, image, rectangle)
        #face = image[y:y + h, x:x + w]
        image_copy = image.copy()
        image_copy[y:y + h, x:x + w] = 0
        return faceAligned, image_copy
