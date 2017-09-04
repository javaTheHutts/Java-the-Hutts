import cv2
import base64
import numpy as np
from image_processing.sample_extract import FaceExtractor
from imutils.convenience import url_to_image
from flask import jsonify, make_response
from hutts_utils.hutts_logger import logger


def grab_image(path=None, stream=None, url=None):
    """
    This function grabs the image from URL, or image path and applies necessary changes to the grabbed
    images so that the image is compatible with OpenCV operation.
    Author(s):
        Stephan Nell
    Args:
        path (str): The path to the image if it reside on disk
        stream (str): A stream of text representing where on the internet the image resides
        url(str): Url representing a path to where an image should be fetched.
    Returns:
        (:obj:'OpenCV image'): Image that is now compatible with OpenCV operations
    TODO:
        Return a Json error indicating file not found
    """
    # If the path is not None, then load the image from disk. Example: payload = {"image": open("id.jpg", "rb")}
    if path is not None:
        logger.debug("Grabbing from Disk")
        image = cv2.imread(path)
    # otherwise, the image does not reside on disk
    else:
        # if the URL is not None, then download the image
        if url is not None:
            logger.debug("Downloading image from URL")
            return url_to_image(url)
        # if the stream is not None, then the image has been uploaded
        elif stream is not None:
            # Example: "http://www.pyimagesearch.com/wp-content/uploads/2015/05/obama.jpg"
            logger.debug("Downloading from image stream")
            data = stream.read()
            image = np.asarray(bytearray(data), dtype="uint8")
            image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    return image


def face_extraction_response(image, text_extract_result=None):
    """
    This function converts the extracted cv2 image and converts it
    to a jpg image. Furthermore, the jpg image is converted to
    Base64 jpg type and returned. If text extraction results are provided
    the response will contain the data of text extraction result as well.
    Author(s):
        Stephan Nell
    Args:
        image: The cv2 (numpy) image that should be converted to jpg
        text_extract_result (dict) the extracted text results
    Returns:
        (:obj:'Response'): The response object that contains the information for HTTP transmission
    """
    extractor = FaceExtractor()
    result = extractor.extract(image)
    _, buffer = cv2.imencode('.jpg', result)
    # replace base64 indicator for the first occurrence and apply apply base64 jpg encoding
    logger.info("Converting to Base64")
    jpg_img = ('data:image/jpg;base64' + str(base64.b64encode(buffer)).replace("b", ",", 1)).replace("'", "")
    temp_dict = {"extracted_face": jpg_img}
    if text_extract_result:
        temp_dict["text_extract_result"] = text_extract_result
    data = jsonify(temp_dict)
    # prepare response
    logger.info("Preparing Response")
    response = make_response(data)
    response.mimetype = 'multipart/form-data'
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'

    return response
