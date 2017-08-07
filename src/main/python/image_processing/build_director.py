import os
from image_processing.blur_manager import BlurManager
from image_processing.color_manager import ColorManager
from image_processing.face_manager import FaceDetector
from image_processing.pipeline_builder import PipelineBuilder
from image_processing.thresholding_manager import ThresholdingManager

# Constants path to trained data for Shape Predictor.
SHAPE_PREDICTOR_PATH = "{base_path}/trained_data/shape_predictor_face_landmarks.dat".format(
    base_path=os.path.abspath(os.path.dirname(__file__)))

DESKTOP = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')


class BuildDirector:
    """
    The BuildDirector constructs the Pipeline using the PipelineBuilder
    """
    @staticmethod
    def construct():
        builder = PipelineBuilder()

        blur_manager = BlurManager("median", (9, 9))
        color_manager = ColorManager("extract", "red")
        threshold_manager = ThresholdingManager("adaptive")
        face_detector = FaceDetector(SHAPE_PREDICTOR_PATH)

        builder.set_blur_manager(blur_manager)
        builder.set_color_manager(color_manager)
        builder.set_face_detector(face_detector)
        builder.set_threshold_manager(threshold_manager)

        return builder.get_result()
