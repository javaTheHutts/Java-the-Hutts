import cv2
import imutils
import numpy as np
from imutils.perspective import order_points, four_point_transform
from skimage.filters import threshold_adaptive

class SimplificationManager:
    def __init__(self):
        print("Initialise SimplificationManager")

    def perspectiveTransformation(self, image):
        ratio = image.shape[0] / 500.0
        orig = image.copy()
        image = imutils.resize(image, height=500)

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (5, 5), 0)
        edged = cv2.Canny(gray, 75, 200)

        (_, contours, _) = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:5]
        warped = orig
        # To-Do determine a better solution to this problem when detecting smaller edge.
        contour_area_threshold = 100000
        if cv2.contourArea(contours[0]) > contour_area_threshold:
            for c in contours:
                peri = cv2.arcLength(c, True)
                approx = cv2.approxPolyDP(c, 0.02 * peri, True)

                if len(approx) == 4:
                    screen_contours = approx
                    break

            cv2.drawContours(image, [screen_contours], -1, (0, 255, 0), 2)
            cv2.imshow("Outline", image)
            warped = four_point_transform(orig, screen_contours.reshape(4, 2) * ratio)
        return warped
