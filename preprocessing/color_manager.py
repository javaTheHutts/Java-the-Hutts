import cv2
import numpy as np


class ColorManager:
    def __init__(self, image):
        self.image = image

    def histEqualisation(self, image):
        return cv2.equalizeHist(image)

    def extractChannel(self, image, image_channel="green"):
        (B, G, R) = cv2.split(image)
        zeros = np.zeros(image.shape[:2], dtype="uint8")

        if image_channel == "green":
            return cv2.merge([B, zeros, R])
        elif image_channel == "blue":
            return cv2.merge([zeros, G, R])
        else:
            return cv2.merge([B, G, zeros])

    def blackHat(self, image, rect_kernel_size=(13, 7)):
        rectangle_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, rect_kernel_size)
        return cv2.morphologyEx(image.copy(), cv2.MORPH_BLACKHAT, rectangle_kernel)

    def topHat(self, image, rect_kernel_size=(13, 7)):
        rectangle_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, rect_kernel_size)
        return cv2.morphologyEx(image, cv2.MORPH_TOPHAT, rectangle_kernel)
