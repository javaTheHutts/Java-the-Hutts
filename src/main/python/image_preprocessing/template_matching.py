import cv2
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
                help="path to input image for profile extraction")
args = vars(ap.parse_args())


class TemplateMatching:
    """
    The TemplateMatching class receives template images to identify the type of identification
    that is used in the image.
    Thus you provide it with templates and it will identify whether you used an id card, id book etc.
    """

    def identify(self, src, template):
        """
        This function identifies the src image by searching for the templates provided.
        Author(s):
            Marno Hermann
        Args:
            Image : File path to the image that needs to be identified
            Tuple list: Each tuple has 4 elements width of image from where template was extracted,
                        the path to the template, threshold value to identify object in the range (0,1),
                        type you want returned as your identifier.
        Returns:
            dict obj: Returns a type if no type could be identified, None is returned
        Todo:
            Explain to others how to use and sort the thresholds in descending order.

        Example usage:
        identify(args["image"],[(1034,"temp_flag.jpg",0.75,"idcard"),(875,"pp2.jpg",0.60,"idbook")])
        """

        # load the source and template image
        source = cv2.imread(src)
        val = []
        for (h, temp, t, n) in template:
            templ = cv2.imread(temp)
            r = h / source.shape[1]
            dim = (h, int(source.shape[0] * r))
            resized = cv2.resize(source, dim, interpolation=cv2.INTER_AREA)

            (tempH, tempW) = templ.shape[:2]

            # find the template in the source image
            result = cv2.matchTemplate(resized, templ, cv2.TM_CCOEFF_NORMED)

            (minVal, maxVal, minLoc, (x, y)) = cv2.minMaxLoc(result)

            val = val + [(maxVal, t, n)]

        for (m, s, n) in val:
            if (m > s):
                print(n)
                return {'type': n}

        return {'type': None}


tm = TemplateMatching()
obj = tm.identify(args["image"], [(1034, "templates/temp_flag.jpg", 0.75, "idcard"), (875, "templates/wap.jpg", 0.60, "idbook"),(1280, "templates/pp2.jpg", 0.65, "studentcard")])

image = cv2.imread(args["image"])
(cx, cy) = image.shape[:2]
cv2.putText(image, "{}".format(obj['type']), (int(cy / 2), 60), cv2.FONT_HERSHEY_SIMPLEX,
            2.0, (0, 255, 0), 3)
cv2.imshow(obj['type'], image)

cv2.waitKey(0)
