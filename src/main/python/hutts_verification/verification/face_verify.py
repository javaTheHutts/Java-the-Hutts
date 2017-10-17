"""
A class that is used to extract and compare two images of faces and calculate the resulting match.
"""

import dlib
from scipy.spatial import distance
from hutts_verification.utils.hutts_logger import logger

__author__ = "Stephan Nell"
__copyright__ = "Copyright 2017, Java the Hutts"
__license__ = "BSD"
__maintainer__ = "Stephan Nell"
__email__ = "nellstephanj@gmail.com"
__status__ = "Development"


class FaceVerify:
    """
    The FaceVerify class is responsible for

    1. Detecting the face.
    2. Generating a threshold value that determines the likeness of two individuals in an image.

    """
    def __init__(self, shape_predictor_path, face_recognition_path):
        """
        Initialise face verify manager.

        :param shape_predictor_path (str): The path to the shape predictor trained data.
        :param face_recognition_path (str): The path to the face recognition trained data.

        Raises:
            - TypeError: If a string value is not passed for shape_predictor_path.
            - TypeError: If a string value is not passed for face_recognition_path.

        """
        logger.info("Initialise FaceVerify")

        if not isinstance(shape_predictor_path, str):
            raise TypeError(
                'Bad type for arg shape_predictor_path - expected string. Received type "%s".' %
                type(shape_predictor_path).__name__
            )

        if not isinstance(face_recognition_path, str):
            raise TypeError(
                'Bad type for arg face_recognition_path - expected string. Received type "%s".' %
                type(face_recognition_path).__name__
            )

        self.shape_predictor_path = shape_predictor_path
        self.face_recognition_path = face_recognition_path

    def verify(self, face1, face2, threshold=0.55):
        """
        This function determines a percentage value of how close the faces
        in the images passed are to each other if the determined value if below
        the threshold value passed by the user a boolean value of True is returned
        indicating that the faces in the images passed indeed match.

        The verify function makes use of the dlib library which guarantees 99.38%
        accuracy on the standard Labeled Faces in the Wild benchmark.

        :param face1 (obj): The first image containing the face that should be compared.
        :param face2 (obj): The second image containing the face that should be compared.
        :param threshold (float): The threshold value determines at what distance the two images
                are considered the same. If a verify score is below the threshold value the faces are
                considered a match. The Labled Faces in the Wild benchmark recommend a default threshold
                of 0.6 but a threshold of 0.55 was decided on to ensure higher confidence in results.

        Returns:
            - (boolean): Represents if two face indeed match.
            - (float): The Euclidean distance between the vector representations of the two faces.

        Raises:
            - ValueError: If no face can be detected then no faces can be matched and the operation should be aborted.

        """

        logger.debug('Getting frontal face detector')
        detector = dlib.get_frontal_face_detector()
        logger.debug('Getting shape predictor')
        shape_predictor = dlib.shape_predictor(self.shape_predictor_path)
        logger.debug('Getting facial recogniser')
        facial_recogniser = dlib.face_recognition_model_v1(self.face_recognition_path)

        logger.info('Getting face in first image')
        face_detections = detector(face1, 1)
        if len(face_detections) == 0:
            logger.error('Could not find a face in the first image')
            raise ValueError('Face could not be detected')
        logger.debug('Getting the shape')
        shape = shape_predictor(face1, face_detections[0])
        logger.debug('Getting the first face descriptor')
        face_descriptor1 = facial_recogniser.compute_face_descriptor(face1, shape)

        logger.info('Getting face in second image')
        face_detections = detector(face2, 1)
        if len(face_detections) == 0:
            logger.error('Could not find a face in the first image')
            raise ValueError('Face could not be detected')
        logger.debug('Getting the shape')
        shape = shape_predictor(face2, face_detections[0])
        logger.debug('Getting the second face descriptor')
        face_descriptor2 = facial_recogniser.compute_face_descriptor(face2, shape)

        logger.info('Calculating the euclidean distance between the two faces')
        match_distance = distance.euclidean(face_descriptor1, face_descriptor2)
        logger.info('Matching distance: ' + str(match_distance))

        # Any distance below our threshold of 0.55 is a very good match.
        # We map 0.55 to 85% and 0 to 100%.
        if match_distance < threshold:
            match_distance = 1 - match_distance
            threshold = 1 - threshold + 0.05
            percentage_match = ((match_distance-threshold)*15/50)*100 + 85
            logger.info('Matching percentage: ' + str(percentage_match) + "%")
            return True, percentage_match
        elif match_distance < threshold + 0.05:
            # In this if we map (0.55-0.60] we map 0.549 to 70% match
            match_distance = 1 - match_distance
            threshold = 1 - threshold + 0.05
            percentage_match = ((match_distance-threshold)*30/55)*100 + 70
            logger.info('Matching percentage: ' + str(percentage_match) + "%")
            return True, percentage_match
        else:
            # If the distance is higher than 0.65 we map it to 60% and below
            percentage_match = 60 - ((match_distance-threshold)*60/40)*100
            logger.info('Matching percentage: ' + str(percentage_match) + "%")
            return False, percentage_match
