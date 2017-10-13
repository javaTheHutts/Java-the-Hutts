"""
The class that is responsible for creating a Pipeline. This class is the Builder
of the Builder design pattern.
"""

from image_preprocessing.pipeline import Pipeline

__author__ = "Nicolai van Niekerk"
__copyright__ = "Copyright 2017, Java the Hutts"
__license__ = "BSD"
__maintainer__ = "Nicolai van Niekerk"
__email__ = "nicvaniek@gmail.com"
__status__ = "Development"


class PipelineBuilder:
    """
    The PipelineBuilder will assemble all the parts of the Pipeline
    """
    def __init__(self):
        """
        Initialize Builder
        """
        self.pipeline = Pipeline()

    def set_blur_manager(self, value):
        """
        This function adds the specified blur manager to the pipeline

        Args:
            value (:BlurManager): BlurManager object to be added

        Returns:
            None
        """
        self.pipeline.blur_manager = value

    def set_color_manager(self, value):
        """
        This function adds the specified color manager to the pipeline

        Args:
            value (:ColorManager): ColorManager object to be added

        Returns:
            None
        """
        self.pipeline.color_manager = value

    def set_threshold_manager(self, value):
        """
        This function adds the specified threshold manager to the pipeline

        Args:
            value (:ThresholdManager): ThresholdManager object to be added

        Returns:
            None
        """
        self.pipeline.threshold_manager = value

    def set_face_detector(self, value):
        """
        This function adds the specified face detector to the pipeline

        Args:
            value (:FaceDetector): FaceDetector object to be added

        Returns:
            None
        """
        self.pipeline.face_detector = value

    def get_result(self):
        """
        This function returns the fully-assembled pipeline

        Returns:
            :Pipeline (Assembled pipeline)
        """
        return self.pipeline
