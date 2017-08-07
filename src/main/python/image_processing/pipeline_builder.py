from main.python.image_processing.pipeline import Pipeline

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
        self.pipeline.blur_manager = value

    def set_color_manager(self, value):
        self.pipeline.color_manager = value

    def set_simplification_manager(self, value):
        self.pipeline.simplification_manager = value

    def set_barcode_manager(self, value):
        self.pipeline.barcode_manager = value

    def set_threshold_manager(self, value):
        self.pipeline.threshold_manager = value

    def set_face_detector(self, value):
        self.pipeline.face_detector = value

    def get_result(self):
        return self.pipeline
