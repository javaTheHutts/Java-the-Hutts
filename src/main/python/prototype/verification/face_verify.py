import dlib
import cv2
from scipy.spatial import distance

class FaceVerify:
    """
    The FaceVerify class is responsible for
    1. Detecting the face.
    2. Generating a threshold value that determines the likeness
    of two individuals in an image
    """
    def __init__(self, shape_predictor_path, face_recognition_path):
        """
        Initialise face verify manager
        Args:
            shape_predictor_path (str): Describes the path the Shape Predictor
            trained data.
            face_recognition_path (str): Describes the path the face recognition
            trained data.
        """
        print("Initialise FaceVerify")
        self.shape_predictor_path = shape_predictor_path
        self.face_recognition_path = face_recognition_path

    def verify(self, image1, image2, threshold=0.55):
        """
        This function determines a percentage value of how close the faces
        in the images passed are to each other if the determined value if below
        the threshold value passed by the user a boolean value of True is returned
        indicating that the faces in the images passed indeed match.

        The Verify function makes use of the dlib library which guarantees 99.38%
        accuracy on the standard Labeled Faces in the Wild benchmark.
        Author(s):
            Stephan Nell
        Args:
            image1 (:obj:'OpenCV image'): The first image containing the face that should be compared.
            image2 (:obj:'OpenCV image'): The second image containing the face that should be compared
            threshold (float): The threshold value determines at what distance the two images are
                considered the same person. If a verify score is below the threshold value the faces are
                considered a match. The Labled Faces in the Wild benchmark recommend a default threshold
                of 0.6 but a threshold of 0.55 was decided on since a threshold of 0.55 represents
                the problem better.

        Returns:
            bool: Represent if two face indeed match True if distance calculated is
                    below threshold value. False if the distance calculated is
                    above threshold value.
            float: Return Euclidean distance between the vector representation
            of the two faces

        Raises:
            ValueError: If no face can be detected no faces can be matched and
            operation should be aborted.
        """
        image1 = cv2.cvtColor(image1, cv2.COLOR_GRAY2RGB)
        image2 = cv2.cvtColor(image2, cv2.COLOR_GRAY2RGB)

        detector = dlib.get_frontal_face_detector()
        shape_predictor = dlib.shape_predictor(self.shape_predictor_path)
        facial_recogniser = dlib.face_recognition_model_v1(self.face_recognition_path)

        face_detections = detector(image1, 1)
        if face_detections is None:
            raise ValueError('Face could not be detected')
        shape = shape_predictor(image1, face_detections[0])
        face_descriptor1 = facial_recogniser.compute_face_descriptor(image1, shape)

        face_detections = detector(image2, 1)
        if face_detections is None:
            raise ValueError('Face could not be detected')
        shape = shape_predictor(image2, face_detections[0])
        face_descriptor2 = facial_recogniser.compute_face_descriptor(image2, shape)

        match_distance = distance.euclidean(face_descriptor1, face_descriptor2)
        print(match_distance)
        if match_distance < threshold:
            return True, match_distance
        else:
            return False, match_distance
