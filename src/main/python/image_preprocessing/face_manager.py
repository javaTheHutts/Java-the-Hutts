from imutils.face_utils import FaceAligner
from imutils.face_utils import rect_to_bb
import dlib
import cv2


class FaceDetector:
    """
    The FaceDetector class is responsible for
    1. Detecting the face.
    2. Extracting a face from an image.
    3. Applying blurring on a detected face in an image.
    """
    def __init__(self, shape_predictor_path):
        """
        Initialise Face Detector Manager.
        Authors(s):
            Nicolai van Niekerk, Stephan Nell
        Args:
            shape_predictor_path (str): Describes the path the Shape Predictor
            trained data.
        Returns:
            None

        """
        self.shape_predictor_path = shape_predictor_path

    def face_likeness_extraction(self, image):
        """
        This function find a face in the image passed and is optimised
        to align the face before being returned.
        Author(s):
            Stephan Nell
        Args:
            image (:obj:'OpenCV image'): Image containing the face we need to detect and extract.
        Raises:
            ValueError: If no face can be detected.
        Returns:
            obj:'OpenCV image': Any background and unnecessary components are removed and only
            the aligned face is returned in gray scale for facial likeness.
        Todo:
            Return error if no face detected

        """
        rectangle = self.detect(image)
        predictor = dlib.shape_predictor(self.shape_predictor_path)
        face_aligner = FaceAligner(predictor, desiredFaceWidth=256)
        face_aligned = face_aligner.align(image, image, rectangle)
        gray_face = cv2.cvtColor(face_aligned, cv2.COLOR_BGR2GRAY)
        return gray_face

    def detect(self, image):
        """
        This function detects the face in the image passed.
        By making use of the dlib HOG feature image_preprocessing and linear classifier for frontal face detection
        we are able to detect the face with less false-positive results and without a major time penalty.
        More Information dlib frontal_face detection: http://dlib.net/imaging.html#get_frontal_face_detector
        Author(s):
            Stephan Nell
        Args:
            image (:obj:'OpenCV image'): Image containing the face we need to detect.
        Raises:
            ValueError: If no face can be detected.
        Returns:
            Integer List: This list contains the box coordinates for the region in which the face resides.
        Todo:
            Return error if no face detected

        """
        detector = dlib.get_frontal_face_detector()
        rectangles = detector(image, 1)
        return rectangles[0]

    def extract_face(self, image):
        """
        This function find a face in the image passed and is optimised
        to align the face before being returned.
        Author(s):
            Stephan Nell
        Args:
            image (:obj:'OpenCV image'): Image containing the face we need to detect and extract.
        Raises:
            ValueError: If no face can be detected.
        Returns:
            obj:'OpenCV image': Any background and unnecessary components are removed and only
            the aligned face is returned.
            obj:'OpenCV image': A copy of the original image is returned.
        Todo:
            Return error if no face detected

        """
        rectangle = self.detect(image)
        predictor = dlib.shape_predictor(self.shape_predictor_path)
        face_aligner = FaceAligner(predictor, desiredFaceWidth=256)
        face_aligned = face_aligner.align(image, image, rectangle)
        image_copy = image.copy()
        return face_aligned, image_copy

    def blur_face(self, image):
        """
        This function find the faces and apply a blurring effect on the detected region.
        After the region has been blurred, the blurred region is reapplied to the original image.
        Blurring the face is implemented as a method in the attempt to reduce noise when extracting
        text from the image later in the image pipeline.
        Author(s):
            Stephan Nell
        Args:
            image (:obj:'OpenCV image'): Image containing the face we need to detect and blur.
        Raises:
            ValueError: If no face can be detected.
        Returns:
            obj:'OpenCV image': A copy of the original image is returned but with the applied
            blurring to the face region.
        Todo:
            Return error if no face detected.
            Remove hard coded y and h adjustment values.

        """
        # We make a deep copy of an image to avoid problems with shallow copies.
        image_copy = image.copy()
        rectangle = self.detect(image)
        (x, y, w, h) = rect_to_bb(rectangle)
        # To Extend the entire region of face since face detector does not include upper head.
        y = y-75
        h = h+75
        sub_face = image[y:y + h, x:x + w]
        sub_face = cv2.dilate(sub_face, None, iterations=3)
        sub_face = cv2.GaussianBlur(sub_face, (31, 31), 0)
        image_copy[y:y + sub_face.shape[0], x:x + sub_face.shape[1]] = sub_face
        return image_copy
