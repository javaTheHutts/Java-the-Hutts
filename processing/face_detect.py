import cv2


class FaceDetector:
    def __init__(self, face_cascade_path):
        self.faceCascade = cv2.CascadeClassifier(face_cascade_path)

    def detect(self, image, scale_factor=1.1, min_neighbors=5, min_size=(30, 30)):
        rectangles = self.faceCascade.detectMultiScale(image, scaleFactor=scale_factor,
                                                  minNeighbors=min_neighbors, minSize=min_size,
                                                  flags=cv2.CASCADE_SCALE_IMAGE)
        return rectangles

    def HOG(self):
        print("HOG still to be implemented")

    def removeFace(self, image):
        rectangle_dimensions = self.detect(image)
        if len(rectangle_dimensions) > 0:
            (x, y, w, h) = max(rectangle_dimensions, key=lambda b: (b[2] * b[3]))
        # To Do if no face found return error
        face = image[y:y + h, x:x + w]
        image_copy = image.copy()
        image_copy[y:y + h, x:x + w] = 0
        return face, image_copy
