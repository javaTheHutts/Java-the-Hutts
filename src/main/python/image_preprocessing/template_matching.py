import cv2
import os

DESKTOP = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')


class TemplateMatching:
    """
    The TemplateMatching class receives template images to identify the type of identification
    that is used in the image.
    Thus you provide it with templates and it will identify whether you used an id card, id book etc.
    Line 16 that specifies my parameters are all pointing to the desktop my template folder needs
    to be added to the site packages.
    """

    def __init__(self):
        self.template = [(1034, DESKTOP + "/templates/temp_flag.jpg", 0.75, "idcard"),
                         (875, DESKTOP + "/templates/wap.jpg", 0.60, "idbook"),
                         (1280, DESKTOP + "/templates/pp2.jpg", 0.60, "studentcard")]

    def identify(self, src):
        """
        This function identifies the src image by searching for the templates provided.
        Author(s):
            Marno Hermann
        Args:
            Image : The image that needs to be identified
            Tuple list: Each tuple has 4 elements width of image from where template was extracted,
                        the path to the template, threshold value to identify object in the range (0,1),
                        type you want returned as your identifier.
        Returns:
            dict obj: Returns a type if no type could be identified, None is returned
        Todo:
            Explain to others how to use and sort the thresholds in descending order.

        Example usage:
        identify(args["image"],[(1034,"temp_flag.jpg",0.75,"idcard"),(875,"pp2.jpg",0.60,"idbook")])
        """

        # load the source and template image
        source = src
        template_objects = []
        for (original_template_image_width, template_path, threshold, object_identifier) in self.template:
            template_image = cv2.imread(template_path)

            ratio = original_template_image_width / source.shape[1]
            dimension = (original_template_image_width, int(source.shape[0] * ratio))
            resized = cv2.resize(source, dimension, interpolation=cv2.INTER_AREA)

            # find the template in the source image
            result = cv2.matchTemplate(resized, template_image, cv2.TM_CCOEFF_NORMED)

            (_, maximum_value, minLoc, (x, y)) = cv2.minMaxLoc(result)

            template_objects = template_objects + [(maximum_value, threshold, object_identifier)]

        for (max, threshold_value, object_type) in template_objects:
            if (max > threshold_value):
                print(object_type)
                return {'type': object_type}

        return {'type': None}
