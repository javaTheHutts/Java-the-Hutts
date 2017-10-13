"""
Wraps the functionality required to dynamically deduce the type of identification
documentation that has been provided in an image.
"""

import cv2
import os
import numpy as np
import imutils
from pathlib import Path
from hutts_verification.utils.hutts_logger import logger
from hutts_verification.utils.pypath import correct_path

__author__ = "Marno Hermann"
__copyright__ = "Copyright 2017, Java the Hutts"
__license__ = "BSD"
__maintainer__ = "Marno Hermann"
__email__ = "marno@barnton-consulting.co.za"
__status__ = "Development"

TEMPLATE_DIR = correct_path(Path(os.path.abspath(os.path.dirname(__file__)), 'templates'))


class TemplateMatching:
    """
    The TemplateMatching class receives template images to identify the type of identification
    that is used in the image.
    Thus you provide it with templates and it will identify whether you used an id card, id book etc.
    """
    def __init__(self):
        logger.debug("Looking for the templates in directory: " + str(TEMPLATE_DIR))
        self.template = [(1034, cv2.imread(TEMPLATE_DIR + "/temp_flag.jpg"), 0.75, "idcard"),
                         (875, cv2.imread(TEMPLATE_DIR + "/wap.jpg"), 0.60, "idbook"),
                         (1280, cv2.imread(TEMPLATE_DIR + "/pp2.jpg"), 0.60, "studentcard")]

    def identify(self, source):
        """
        This function identifies the src image by searching for the templates provided.

        Args:
            source (Image) : The image that needs to be identified

        Returns:
            string : Returns a string if no type could be identified, None is returned

        :Example:
        identify(args["image"]]) !

        """
        if hasattr(source, 'shape') is False:
            raise TypeError("Must be an image")
        # load the source and template image
        for (original_template_image_width, template_image, threshold, object_identifier) in self.template:
            ratio = original_template_image_width / source.shape[1]
            dimension = (original_template_image_width, int(source.shape[0] * ratio))
            resized = cv2.resize(source, dimension, interpolation=cv2.INTER_AREA)
            if resized.shape[0] < template_image.shape[0] or resized.shape[1] < template_image.shape[1]:
                return 'None'
            # find the template in the source image
            result = cv2.matchTemplate(resized, template_image, cv2.TM_CCOEFF_NORMED)

            (_, maximum_value, _, _) = cv2.minMaxLoc(result)

            if maximum_value > threshold:
                logger.info(object_identifier)
                return object_identifier
        # first two parameters create a range of [0.8;1.8]. 10 specifies that we want to split the
        # range in 20 equal sizes. Each of them is used as a ratio value to get different image sizes.
        # [::-1] just reverses the np array to start from 1.8 and down to 0.8.
        for scale in np.linspace(0.8, 1.8, 10)[::-1]:
            # resize the image according to the scale, and keep track
            # of the ratio of the resizing
            resized = imutils.resize(source, width=int(source.shape[1] * scale))
            for (original_template_image_width, template_image, threshold, object_identifier) in self.template:

                # if the resized image is smaller than the template, then break
                # from the loop
                if resized.shape[0] < template_image.shape[0] or resized.shape[1] < template_image.shape[1]:
                    return 'None'

                result = cv2.matchTemplate(resized, template_image, cv2.TM_CCOEFF_NORMED)
                (_, maximum_value, _, _) = cv2.minMaxLoc(result)

                if (maximum_value > threshold):
                    logger.info(object_identifier)
                    return object_identifier

        logger.warning('Unsuccessful template matching attempt')
        return 'None'
