import cv2
import numpy as np


class ColorManager:
    def __init__(self, image):
        self.image = image

    def histEqualisation(self, image):
        equalisation = cv2.equalizeHist(image)
        return equalisation

    def extractChannel(self, image, image_channel="green"):
        (B, G, R) = cv2.split(image)
        zeros = np.zeros(image.shape[:2], dtype="uint8")

        if image_channel == "green":
            return cv2.merge([zeros, G, zeros])
        elif image_channel == "blue":
            return cv2.merge([B, zeros, zeros])
        else:
            return cv2.merge([zeros, zeros, R])
