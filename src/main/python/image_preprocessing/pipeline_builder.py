from image_preprocessing.pipeline import Pipeline


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
        Author(s):
            Nicolai van Niekerk
        Args:
            value (:BlurManager): BlurManager object to be added
        Returns:
            None

        """
        self.pipeline.blur_manager = value

    def set_color_manager(self, value):
        """
        This function adds the specified color manager to the pipeline
        Author(s):
            Nicolai van Niekerk
        Args:
            value (:ColorManager): ColorManager object to be added
        Returns:
            None

        """
        self.pipeline.color_manager = value

    def set_threshold_manager(self, value):
        """
        This function adds the specified threshold manager to the pipeline
        Author(s):
            Nicolai van Niekerk
        Args:
            value (:ThresholdManager): ThresholdManager object to be added
        Returns:
            None

        """
        self.pipeline.threshold_manager = value

    def set_face_detector(self, value):
        """
        This function adds the specified face detector to the pipeline
        Author(s):
            Nicolai van Niekerk
        Args:
            value (:FaceDetector): FaceDetector object to be added
        Returns:
            None

        """
        self.pipeline.face_detector = value

    def get_result(self):
        """
        This function returns the fully-assembled pipeline
        Author(s):
            Nicolai van Niekerk
        Args:
            None
        Returns:
            :Pipeline (Assembled pipeline)

        """
        return self.pipeline
