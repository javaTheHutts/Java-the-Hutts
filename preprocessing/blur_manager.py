import cv2


class BlurManager:
    def __init__(self):
        print("Initialise BlurManager")

    def blur(self, image, blur_kernel=[(3, 3)]):

        for (kX, kY) in blur_kernel:
            blurred = cv2.blur(image, (kX, kY))
        return blurred

    def gaussianBlur(self, image, blur_kernel=[(7, 7)]):

        for (kX, kY) in blur_kernel:
            blurred = cv2.GaussianBlur(image, (kX, kY), 0)
        return blurred

    def medianBlur(self, image, blur_kernel=[3]):
        # To-Do Error Checking for different Kernel sizes
        for k in blur_kernel:
            blurred = cv2.medianBlur(image, k)
        return blurred
