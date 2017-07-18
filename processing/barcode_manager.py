import numpy as np
import cv2
import zbar.misc


class BarCodeManager:
    def __init__(self):
        print("Initialise BarCodeDetector")

    def detect(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        grad_x = cv2.Sobel(gray, ddepth=cv2.CV_32F, dx=1, dy=0, ksize=-1)
        grad_y = cv2.Sobel(gray, ddepth=cv2.CV_32F, dx=0, dy=1, ksize=-1)

        gradient = cv2.subtract(grad_x, grad_y)
        gradient = cv2.convertScaleAbs(gradient)

        blurred = cv2.blur(gradient, (7, 7))
        (_, thresh) = cv2.threshold(blurred, 225, 255, cv2.THRESH_BINARY)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (27, 7))
        closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

        eroded = cv2.erode(closed, None, iterations=4)
        dilated = cv2.dilate(eroded, None, iterations=4)

        (_, contours, _) = cv2.findContours(dilated.copy(), cv2.RETR_EXTERNAL,
                                            cv2.CHAIN_APPROX_SIMPLE)
        c = sorted(contours, key=cv2.contourArea, reverse=True)[0]

        rectangle = cv2.minAreaRect(c)
        box = cv2.boxPoints(rectangle)
        box = np.int0(box)
        (x, y, w, h) = cv2.boundingRect(box)
        diff = y - (y+h)
        if abs(diff) < 200:
            # Valid Barcode not something detected by Noise
            # Add Additional checks
            return True, image[y:y + h, x:x + w], box
        else:
            return False, image, box

    def get_barcode_info(self, image):
        (detection, detected_image, box) = self.detect(image.copy())
        if detection:
            gray = cv2.cvtColor(detected_image, cv2.COLOR_BGR2GRAY)
            scanner = zbar.Scanner()
            results = scanner.scan(gray)
            image = self.apply_barcode_blur(image, box)
            if not results:
                return False, "", image
            else:
                return True, results[0].data, image
        else:
            return False, "", image

    def apply_barcode_blur(self, image, box):
        (x, y, w, h) = cv2.boundingRect(box)
        sub_bar_code = image[y:y + h, x:x + w]
        sub_bar_code = cv2.dilate(sub_bar_code, None, iterations=3)
        sub_bar_code = cv2.GaussianBlur(sub_bar_code, (31, 31), 0)
        image[y:y + sub_bar_code.shape[0], x:x + sub_bar_code.shape[1]] = sub_bar_code
        return image
