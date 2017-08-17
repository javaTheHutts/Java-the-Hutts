import cv2
import os

DESKTOP = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')


class TemplateMatching:
    """
    The TemplateMatching class receives template images to identify the type of identification
    that is used in the image.
    Thus you provide it with templates and it will identify whether you used an id card, id book etc.
    """

    def __init__(self):
        self.template = [(1034, DESKTOP + "/templates/temp_flag.jpg", 0.75, "idcard"),
                         (875, DESKTOP + "/templates/wap.jpg", 0.60, "idbook"),
                         (1280, DESKTOP + "/templates/pp2.jpg", 0.60, "studentcard")]

    def identify(self, source):
        """
        This function identifies the src image by searching for the templates provided.
        Author(s):
            Marno Hermann
        Args:
            Image : The image that needs to be identified

        Returns:
            dict obj: Returns a type if no type could be identified, None is returned
        Todo:
            Explain to others how to use and sort the thresholds in descending order.

        Example usage:
        identify(args["image"]])
        """

        # load the source and template image
        for (original_template_image_width, template_path, threshold, object_identifier) in self.template:
            template_image = cv2.imread(template_path)

            ratio = original_template_image_width / source.shape[1]
            dimension = (original_template_image_width, int(source.shape[0] * ratio))
            resized = cv2.resize(source, dimension, interpolation=cv2.INTER_AREA)

            # find the template in the source image
            result = cv2.matchTemplate(resized, template_image, cv2.TM_CCOEFF_NORMED)

            (_, maximum_value, minLoc, (x, y)) = cv2.minMaxLoc(result)

            if (maximum_value > threshold):
                print(object_identifier)
                return object_identifier
        return 'None'
