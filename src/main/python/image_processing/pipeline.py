from main.python.image_processing.blur_manager import BlurManager
from main.python.image_processing.barcode_manager import BarCodeManager
from main.python.image_processing.color_manager import ColorManager
from main.python.image_processing.face_manager import FaceDetector
from main.python.image_processing.simplification_manager import SimplificationManager
from main.python.image_processing.thresholding_manager import ThresholdingManager

class Pipeline:
    """
    The Pipeline will perform all necessary processing on the image and is built by the PipelineBuilder
    """
    def __init__(self, blur_manager, barcode_manager, color_manager, face_detector, simplification_manager, threshold_manager):
        """
        Initialize Pipeline with parameters passed from the Builder
        """
        self.blur_manager = blur_manager
        self.barcode_manager = barcode_manager
        self.color_manager = color_manager
        self.face_detector = face_detector
        self.simplification_manager = simplification_manager
        self.threshold_manager = threshold_manager

    def process(self, image):
        """
        This function applies all the processing needed on the image
        Author(s):
            Stephan Nell, Nicolai van Niekerk
        Args:
            image (:obj:'OpenCV image'): Image to which processing should be applied to.
        Returns:
            image: The processed image
        Todo:

        """