import cv2


class FaceDetector:
    def __init__(self, faceCascadePath):
        self.faceCascade = cv2.CascadeClassifier(faceCascadePath)

    def detect(self, image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)):
        # detect faces in the image
        rects = self.faceCascade.detectMultiScale(image, scaleFactor=scaleFactor,
                                                  minNeighbors=minNeighbors, minSize=minSize,
                                                  flags=cv2.CASCADE_SCALE_IMAGE)

        # return the bounding boxes around the faces in the image
        return rects

    def HOG(self):
        print("HOG still to be implemented")

    def removeFace(self, image):
        rectangle_dimensions = self.detect(image)
        if len(rectangle_dimensions) > 0:
            # sort the bounding boxes, keeping only the largest one
            (x, y, w, h) = max(rectangle_dimensions, key=lambda b: (b[2] * b[3]))
        image[y:y + h, x:x + w] = 0
        face = image[y:y + h, x:x + w]
        return (face, image)
