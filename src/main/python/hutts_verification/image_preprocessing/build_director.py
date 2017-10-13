"""
This class is responsible for controlling the PipelineBuilder.
"""

import os
from hutts_verification.image_preprocessing.blur_manager import BlurManager
from hutts_verification.image_preprocessing.color_manager import ColorManager
from hutts_verification.image_preprocessing.face_manager import FaceDetector
from hutts_verification.image_preprocessing.pipeline_builder import PipelineBuilder
from hutts_verification.image_preprocessing.thresholding_manager import ThresholdingManager
from hutts_verification.utils.hutts_logger import logger
from hutts_verification.utils.pypath import correct_path

__authors__ = "Nicolai van Niekerk, Marno Hermann, Stephan Nell"
__copyright__ = "Copyright 2017, Java the Hutts"
__license__ = "BSD"
__maintainer__ = "Nicolai van Niekerk"
__email__ = "nicvaniek@gmail.com"
__status__ = "Development"

# Constants path to trained data for Shape Predictor.
SHAPE_PREDICTOR_PATH = correct_path("{base_path}/trained_data/shape_predictor_face_landmarks.dat".format(
    base_path=os.path.abspath(os.path.dirname(__file__))))


class BuildDirector:
    """
    The BuildDirector constructs the Pipeline using the PipelineBuilder
    """
    @staticmethod
    def construct_text_extract_pipeline(preferences, identification_type):
        """
        This function constructs the pipeline for text extraction.
        This includes building different managers with their specific parameters.
        These managers will be called within the pipeline when executed.

        Args:
            preferences (dict): User-specified techniques to use in pipeline.
            identification_type (string): Contains the type of identification, this is used
                                        to determine which techniques are used.

        Returns:
            :Pipeline (Constructed pipeline)
        """
        builder = PipelineBuilder()
        # Use template matching to identify type here

        if 'blur_method' in preferences:
            blur_method = preferences['blur_method']
        elif identification_type == 'idcard':
            blur_method = 'gaussian'
        elif identification_type == 'idbook':
            blur_method = 'gaussian'
        elif identification_type == 'studentcard':
            blur_method = 'median'
        else:
            # Default
            blur_method = 'median'

        if blur_method == 'median':
            blur_kernel_size = [3]
        else:
            if identification_type == 'idbook':
                blur_kernel_size = [(3, 3)]
            elif identification_type == 'idcard':
                blur_kernel_size = [(3, 3)]
            else:
                blur_kernel_size = [(3, 3)]

        if 'threshold_method' in preferences:
            threshold_method = preferences['threshold_method']
        elif identification_type == 'idcard':
            threshold_method = 'adaptive'
        elif identification_type == 'idbook':
            threshold_method = 'adaptive'
        elif identification_type == 'studentcard':
            threshold_method = 'adaptive'
        else:
            # Default
            threshold_method = 'adaptive'

        if 'color' in preferences:
            color_extraction_type = 'extract'
            color = preferences['color']
        elif identification_type == 'idcard':
            color_extraction_type = 'extract'
            color = 'red_blue'
        elif identification_type == 'idbook':
            color_extraction_type = 'extract'
            color = 'red_blue'
        elif identification_type == 'studentcard':
            color_extraction_type = 'extract'
            color = 'red'
        else:
            # Default
            color_extraction_type = 'extract'
            color = 'red'

        logger.debug("Blur Method: " + blur_method)
        logger.debug("Kernel Size: " + str(blur_kernel_size))
        logger.debug("ColorXType: " + color_extraction_type)
        logger.debug("Color: " + color)
        logger.debug("Threshold Method: " + threshold_method)

        blur_manager = BlurManager(blur_method, blur_kernel_size)
        color_manager = ColorManager(color_extraction_type, color)
        threshold_manager = ThresholdingManager(threshold_method)
        face_detector = FaceDetector(SHAPE_PREDICTOR_PATH)

        builder.set_blur_manager(blur_manager)
        builder.set_color_manager(color_manager)
        builder.set_face_detector(face_detector)
        builder.set_threshold_manager(threshold_manager)

        return builder.get_result()

    @staticmethod
    def construct_face_extract_pipeline():
        """
        This function constructs the pipeline for face extraction.
        This includes building different managers with their specific parameters.
        These managers will be called within the pipeline when executed.

        Returns:
            :Pipeline (Constructed pipeline)
        """
        logger.debug("Shape Predictor path: " + SHAPE_PREDICTOR_PATH)
        builder = PipelineBuilder()

        face_detector = FaceDetector(SHAPE_PREDICTOR_PATH)
        builder.set_face_detector(face_detector)

        return builder.get_result()
