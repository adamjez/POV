import models
import cv2
import numpy as np
import imutils


class ProcessBall:
    WINDOW_NAME = "ball_detector"
    # for yellow
    # lower = (85, 0, 0)
    # upper = (100, 170, 100)

    lower = [60, 0, 0]
    upper = [90, 40, 255]

    sLow = 60
    sHigh = 160

    def check_keyboard(self):
        ch = 0xFF & cv2.waitKey(1)
        if ch == ord('m'):
            co_je_uvnitr = self.hsv_x[self.point]
            # print("%d, %d" % (self.sLow, self.sHigh))
            print(co_je_uvnitr)
            return True

        elif ch == ord('i'):
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

    point = (375, 465)

    color = np.array([47, 94, 108])

    TEMPLATE_SIZE = 20

    template = None

    def setup_template(self):
        template = np.zeros([2 * self.TEMPLATE_SIZE, 2 * self.TEMPLATE_SIZE], np.uint8)
        cv2.circle(template, (self.TEMPLATE_SIZE, self.TEMPLATE_SIZE), self.TEMPLATE_SIZE, (255, 255, 255), -1)
        im2, circle_contours, hierarchy = cv2.findContours(template, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        self.template = circle_contours[0]

    def __init__(self):
        self.setup_template()

    def create_contours(self, image):
        contours = [np.array(
            [
                [[334, 261]], [[333, 262]], [[332, 262]], [[331, 262]], [[330, 262]], [[329, 262]], [[328, 262]],
                [[327, 262]], [[326, 262]], [[325, 262]], [[324, 262]], [[323, 262]], [[322, 262]], [[321, 263]],
                [[320, 263]], [[319, 264]], [[318, 265]], [[317, 266]], [[316, 267]], [[315, 268]], [[315, 269]],
                [[314, 270]], [[314, 271]], [[313, 272]], [[313, 273]], [[313, 274]], [[313, 275]], [[313, 276]],
                [[313, 277]], [[313, 278]], [[313, 279]], [[313, 280]], [[313, 281]], [[313, 282]], [[313, 283]],
                [[313, 284]], [[313, 285]], [[313, 286]], [[313, 287]], [[314, 288]], [[314, 289]], [[315, 290]],
                [[316, 291]], [[317, 292]], [[318, 293]], [[319, 294]], [[320, 295]], [[321, 295]], [[322, 296]],
                [[323, 297]], [[324, 298]], [[325, 299]], [[326, 299]], [[327, 300]], [[328, 300]], [[329, 300]],
                [[330, 300]], [[331, 300]], [[332, 300]], [[333, 300]], [[334, 300]], [[335, 300]], [[335, 299]],
                [[335, 298]], [[335, 297]], [[335, 296]], [[334, 295]], [[334, 294]], [[334, 293]], [[335, 292]],
                [[336, 291]], [[337, 290]], [[338, 290]], [[339, 289]], [[340, 289]], [[341, 289]], [[342, 289]],
                [[343, 289]], [[344, 290]], [[345, 291]], [[345, 292]], [[345, 293]], [[346, 293]], [[347, 293]],
                [[348, 293]], [[349, 293]], [[350, 293]], [[350, 292]], [[351, 291]], [[352, 291]], [[353, 290]],
                [[354, 289]], [[355, 288]], [[356, 287]], [[356, 286]], [[356, 285]], [[356, 284]], [[356, 283]],
                [[355, 282]], [[355, 281]], [[354, 280]], [[353, 279]], [[352, 278]], [[352, 277]], [[351, 276]],
                [[350, 276]], [[349, 275]], [[348, 274]], [[347, 274]], [[346, 274]], [[345, 273]], [[344, 272]],
                [[343, 271]], [[342, 270]], [[342, 269]], [[342, 268]], [[342, 267]], [[343, 266]], [[344, 266]],
                [[344, 265]], [[344, 264]], [[344, 263]], [[344, 262]], [[343, 262]], [[342, 262]], [[341, 261]],
                [[340, 261]], [[339, 261]], [[338, 261]], [[337, 261]], [[336, 261]], [[335, 261]],
            ],
        ), np.array([[1, 1], [10, 50], [35, 45], [50, 50]], dtype=np.int32)]

        drawing = np.zeros([800, 800], np.uint8)

        min_ret = np.inf
        best_contour = None

        drawing = cv2.cvtColor(drawing, cv2.COLOR_GRAY2RGB)
        for index in range(len(contours)):
            cnt = contours[index]
            cv2.drawContours(drawing, [cnt], 0, (0, 255, 0), 2)

            ret = cv2.matchShapes(cnt, self.template, 1, 0.0)
            if ret < min_ret:
                min_ret = ret
                best_contour = cnt

                # epsilon = 0.1 * cv2.arcLength(cnt, True)
                # approx = cv2.approxPolyDP(cnt, epsilon, True)
                # cv2.drawContours(drawing, [approx], 0, (0, 255, 0), 2)

        cv2.drawContours(drawing, [best_contour], 0, (0, 0, 255), 10)

        cv2.imshow('output', drawing)
        return

    def detect(self, image):
        # self.create_contours(image)
        # return

        hsv = cv2.cvtColor(image.copy(), cv2.COLOR_RGB2HSV)
        hsv = cv2.medianBlur(hsv, 5)
        out = cv2.inRange(hsv, tuple(self.lower), tuple(self.upper))
        out = cv2.erode(out, None, iterations=2)
        out = cv2.dilate(out, None, iterations=2)

        im2, contours, hierarchy = cv2.findContours(out, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

        out = cv2.cvtColor(out, cv2.COLOR_GRAY2RGB)

        min_ret = np.inf
        best_contour = None
        best_circle = None

        # epsilon = 0.1 * cv2.arcLength(cnt, True)
        # approx = cv2.approxPolyDP(cnt, epsilon, True)
        # cv2.drawContours(drawing, [approx], 0, (0, 255, 0), 2)

        for index in range(len(contours)):
            cnt = contours[index]
            if cnt.size < 50:
                continue

            (x, y), radius = cv2.minEnclosingCircle(cnt)
            if radius < 15:
                continue

            center = (int(x), int(y))
            radius = int(radius)

            ret = cv2.matchShapes(cnt, self.template, 1, 0.0)
            if ret < min_ret:
                min_ret = ret
                best_contour = cnt
                best_circle = (center, radius)

            cv2.drawContours(out, [cnt], 0, (0, 200, 0), 2)

            cv2.circle(out, center, radius, (0, 255, 0), 2)
            cv2.putText(out, str(center[0]) + "|" + str(center[1]), center, cv2.QT_FONT_BLACK, 0.5, (0, 0, 255))
            # cv2.circle(image, center, radius, (0, 255, 0), 2)

            # cv2.circle(image, center, 1, (0, 0, 255), 2)

        cv2.drawContours(out, [best_contour], 0, (0, 0, 255), 5)
        if best_circle is not None:
            cv2.circle(image, best_circle[0], best_circle[1], (0, 255, 0), 2)

        cv2.imshow("h", out)
        cv2.imshow("img", image)


def calib_detect(self, image):
    hsv = cv2.cvtColor(image.copy(), cv2.COLOR_RGB2HSV)
    hsv = cv2.medianBlur(hsv, 5)
    self.check_keyboard()
    h, s, v = cv2.split(hsv)

    # self.lower[2] = self.sLow
    # self.upper[2] = self.sHigh

    # print(self.lower[2], self.upper[2])

    # hBin = cv2.inRange(h, self.lower[0], self.upper[0])
    # sBin = cv2.inRange(s, self.lower[1], self.upper[1])
    # vBin = cv2.inRange(v, self.lower[2], self.upper[2])

    v = cv2.inRange(hsv, tuple(self.lower), tuple(self.upper))

    cv2.imshow("h", v)
    # cv2.imshow("s", vBin)


def detect_checking_deprecated(self, image):
    self.check_keyboard()
    hsv = cv2.cvtColor(image.copy(), cv2.COLOR_RGB2HSV)
    # print(hsv[self.point[0],self.point[1]],)
    # return

    # self.hsv_x = hsv
    # cv2.circle(hsv, self.point, 5, (0, 0, 255))

    lower_border_arr = self.color - [20, 20, 20]
    upper_border_arr = self.color + [20, 20, 20]

    lower_border = tuple(lower_border_arr.tolist())
    upper_border = tuple(upper_border_arr.tolist())
    mask = cv2.inRange(hsv, lower_border, upper_border)

    self.draw(mask)
    pass


def draw(self, image):
    cv2.imshow(self.WINDOW_NAME, image)


def detect_template_attempt(self, image):
    template = cv2.imread("./template.png", 1)
    w, h, type = template.shape
    # cv2.imshow("asd", template)
    # cv2.waitkey

    method = cv2.TM_SQDIFF

    res = cv2.matchTemplate(image, template, method)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
    if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
        top_left = min_loc
    else:
        top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)
    cv2.rectangle(image, top_left, bottom_right, 255, 2)

    cv2.imshow("achjo", image)


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
