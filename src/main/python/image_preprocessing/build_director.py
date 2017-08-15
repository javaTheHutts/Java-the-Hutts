import os
from image_preprocessing.blur_manager import BlurManager
from image_preprocessing.color_manager import ColorManager
from image_preprocessing.face_manager import FaceDetector
from image_preprocessing.pipeline_builder import PipelineBuilder
from image_preprocessing.thresholding_manager import ThresholdingManager

# Constants path to trained data for Shape Predictor.
SHAPE_PREDICTOR_PATH = "{base_path}/trained_data/shape_predictor_face_landmarks.dat".format(
    base_path=os.path.abspath(os.path.dirname(__file__)))

DESKTOP = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')


class BuildDirector:
    """
    The BuildDirector constructs the Pipeline using the PipelineBuilder
    """
    @staticmethod
    def construct(preferences):
        """
        This function constructs the pipeline
        Author(s):
            Nicolai van Niekerk
        Args:
            preferences (dict): User-specified techniques to use in pipeline.
        Returns:
            :Pipeline (Constructed pipeline)
        """
        builder = PipelineBuilder()

        if 'blur_method' in preferences:
            blur_method = preferences['blur_method']
        else:
            # Default
            blur_method = 'median'

        if blur_method == 'median':
            blur_kernel_size = [9]
        else:
            blur_kernel_size = [(3, 3)]

        if 'threshold_method' in preferences:
            threshold_method = preferences['threshold_method']
        else:
            # Default
            threshold_method = 'adaptive'

        if 'color' in preferences:
            color_extraction_type = 'extract'
            color = preferences['color']
        else:
            # Default
            color_extraction_type = 'extract'
            color = 'red'

        print("Blur Method: " + blur_method)
        print("Kernel Size: " + str(blur_kernel_size))
        print("ColorXType: " + color_extraction_type)
        print("Color: " + color)
        print("Threshold Method: " + threshold_method)

        blur_manager = BlurManager(blur_method, blur_kernel_size)
        color_manager = ColorManager(color_extraction_type, color)
        threshold_manager = ThresholdingManager(threshold_method)
        face_detector = FaceDetector(SHAPE_PREDICTOR_PATH)

        builder.set_blur_manager(blur_manager)
        builder.set_color_manager(color_manager)
        builder.set_face_detector(face_detector)
        builder.set_threshold_manager(threshold_manager)

        return builder.get_result()
