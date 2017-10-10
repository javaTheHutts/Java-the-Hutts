from imutils.face_utils import FaceAligner
from imutils.face_utils import rect_to_bb
from hutts_utils.hutts_logger import logger
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
        self.predictor = dlib.shape_predictor(self.shape_predictor_path)
        self.detector = dlib.get_frontal_face_detector()
        self.face_aligner = FaceAligner(self.predictor, desiredFaceWidth=256)

    def detect(self, image):
        """
        This function detects the face in the image passed.
        By making use of the dlib HOG feature image_preprocessing and linear classifier for frontal face detection
        we are able to detect the face with less false-positive results and without a major time penalty.
        More Information dlib frontal_face detection: http://dlib.net/imaging.html#get_frontal_face_detector

        A check will be done to see if a face is present in the image.
        If a face is not detected in the image the execution should log that the face was not found and continue
        with execution. This is due to the fact that face detection might not be critical to
        a function (like with text extraction) and rather be used to increase accuracy.
        Author(s):
            Stephan Nell
        Args:
            image (:obj:'OpenCV image'): Image containing the face we need to detect.
        Raises:
            ValueError: If no face can be detected.
        Returns:
            Integer List: This list contains the box coordinates for the region in which the face resides.
        """
        rectangles = self.detector(image, 1)
        if len(rectangles) == 0:
            logger.warning('No valid face found. Original image will be returned')
        return rectangles[0]

    def extract_face(self, image):
        """
        This function finds a face in the image passed and is optimised
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
        """
        rectangle = self.detect(image)
        face_aligned = self.face_aligner.align(image, image, rectangle)
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
