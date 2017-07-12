from skimage.filters import threshold_adaptive
import argparse
import cv2


class ThresholdingManager:
    def __init__(self, image):
        self.image = image

    def adaptiveThresholding(self, image, blur_method=None, blur_kernel=(5, 5)):
        thresh = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 25, 15)
        return thresh

    def otsuThresholding(self, image, blur_method="gaussian", blur_kernel=(7, 7)):
        (_, threshInv) = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
        return threshInv
