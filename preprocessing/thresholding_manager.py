import cv2


class ThresholdingManager:
    def __init__(self, image):
        self.image = image

    def adaptiveThresholding(self, image):
        return cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 25, 15)

    def otsuThresholding(self, image):
        (_, threshInv) = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
        return threshInv
