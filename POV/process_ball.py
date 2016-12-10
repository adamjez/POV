import models
import cv2
import numpy as np
import imutils


class ProcessBall:
    # for yellow
    # lower = (85, 0, 0)
    # upper = (100, 170, 100)

    lower = (60, 10, 60)
    upper = (80, 30, 160)

    sLow = 60
    sHigh = 160

    def check_keyboard(self):
        ch = 0xFF & cv2.waitKey(1)
        if ch == ord('i'):
            self.sLow += 1
            return True
        elif ch == ord('k'):
            self.sLow -= 1
            return True

        elif ch == ord('o'):
            self.sHigh += 1
            return True

        elif ch == ord('l'):
            self.sHigh -= 1
            return True

        # print("%d, %d" % (self.sLow, self.sHigh))

        return False

    def detect(self, image):
        self.detect_white(image)

    def detect_white(self, image):

        self.check_keyboard()

        hsv = cv2.cvtColor(image.copy(), cv2.COLOR_RGB2HSV)
        hsv = cv2.medianBlur(hsv, 5)

        h, s, v = cv2.split(hsv)

        hBin = cv2.inRange(h, self.lower[0], self.upper[0])
        sBin = cv2.inRange(s, self.lower[1], self.upper[1])
        # vBin = np.invert(cv2.inRange(v, self.lower[2], self.upper[2]))

        out = np.bitwise_and(hBin, sBin)
        out = cv2.erode(out, None, iterations=2)
        out = cv2.dilate(out, None, iterations=2)

        im2, contours, hierarchy = cv2.findContours(out, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

        out = cv2.cvtColor(out, cv2.COLOR_GRAY2RGB)

        for index in range(len(contours)):
            cnt = contours[index]
            if cnt.size < 150:
                continue

            cv2.drawContours(out, [cnt], 0, (255, 0, 0), 2)
            (x, y), radius = cv2.minEnclosingCircle(cnt)
            center = (int(x), int(y))
            radius = int(radius)
            cv2.circle(image, center, radius, (0, 255, 0), 2)

        cv2.imshow("OUT", out)
        cv2.imshow("S", image)

    def detect_yellow(self, image):
        """
        Kinda works with yellow ball (game01)
        :param image:
        :return:
        """

        hsv = cv2.cvtColor(image.copy(), cv2.COLOR_RGB2HSV)
        # hsv = cv2.medianBlur(hsv, 5)

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

            cv2.drawContours(image, [contours[index]], 0, (255, 0, 0), 2)

        cv2.imshow("detected_by_range", image)

        return models.Ball((0, 0), 0, 0)
