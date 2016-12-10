import models
import cv2
import numpy as np
import imutils


class ProcessBall:
    lower = (85, 0, 0)
    upper = (100, 170, 100)

    background = None

    sLow = 0
    sHigh = 100

    def detect(self, image):
        if self.background is None:
            self.background = image
            # hsv = cv2.cvtColor(image.copy(), cv2.COLOR_RGB2HSV)
            # cv2.imshow("ahoj", hsv)

        self.detect_by_range(image)

    def detect_by_range(self, image):
        """
        Kinda works with yellow ball (game01)
        :param image:
        :return:
        """
        if self.background is None:
            self.background = image

        hsv = cv2.cvtColor(image.copy(), cv2.COLOR_RGB2HSV)
        # hsv = cv2.medianBlur(hsv, 5)

        # cv2.imshow("asdf", hsv)
        # return

        h, s, v = cv2.split(hsv)

        hBin = cv2.inRange(h, self.lower[0], self.upper[0])
        sBin = np.invert(cv2.inRange(s, self.lower[1], self.upper[1]))
        vBin = np.invert(cv2.inRange(v, self.lower[2], self.upper[2]))

        out = np.bitwise_and(np.bitwise_and(hBin, sBin), vBin)

        out = cv2.erode(out, None, iterations=2)
        out = cv2.dilate(out, None, iterations=2)

        im2, contours, hierarchy = cv2.findContours(out, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        out = cv2.cvtColor(out, cv2.COLOR_GRAY2RGB)

        for index in range(len(contours)):
            # print("Size %d" % contours[index].size)
            if contours[index].size < 150:
                continue

            cv2.drawContours(image, contours[index], -1, (0, 0, 255), 2)

        cv2.imshow("detected_by_range", image)

        return models.Ball((0, 0), 0, 0)
