from imutils.face_utils import FaceAligner
from imutils.face_utils import rect_to_bb
import dlib
import cv2

class FaceDetector:
    def __init__(self, shape_predictor_path):
        print("Initialise FaceDetector")
        self.shape_predictor_path = shape_predictor_path

    def detect(self, image):
        # To Do if no face found return error
        detector = dlib.get_frontal_face_detector()
        rectangles = detector(image, 1)
        return rectangles[0]

    def extract_face(self, image):
        rectangle = self.detect(image)
        predictor = dlib.shape_predictor(self.shape_predictor_path)
        face_aligner = FaceAligner(predictor, desiredFaceWidth=256)
        face_aligned = face_aligner.align(image, image, rectangle)
        image_copy = image.copy()
        return face_aligned, image_copy

    def blur_face(self, image):
        image_copy = image.copy()
        rectangle = self.detect(image)
        (x, y, w, h) = rect_to_bb(rectangle)
        y = y-75
        h = h+75
        sub_face = image[y:y + h, x:x + w]
        sub_face = cv2.dilate(sub_face, None, iterations=3)
        sub_face = cv2.GaussianBlur(sub_face, (31, 31), 0)
        image_copy[y:y + sub_face.shape[0], x:x + sub_face.shape[1]] = sub_face
        return image_copy


