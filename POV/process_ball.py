import cv2
import numpy as np
import models
from drawer import Drawer

DEBUG = False


class ProcessBall:
    BALL_TEMPLATE_SIZE = 20
    MIN_CONTOUR_SIZE = 10
    MIN_CONTOUR_RADIUS = 7

    ball_template = None

    ball_hsv_color = np.array([121, 193, 164])
    ball_low_corr = np.array([50, 50, 50])  # TODO maybe tweak the corrections
    ball_up_corr = np.array([20, 20, 20])

    def check_keyboard(self):
        ch = 0xFF & cv2.waitKey(1)
        if ch == ord('i'):
            self.ball_low_corr += np.ones([3], dtype=np.int_)
        elif ch == ord('k'):
            self.ball_low_corr -= np.ones([3], dtype=np.int_)
        elif ch == ord('o'):
            self.ball_up_corr += np.ones([3], dtype=np.int_)
        elif ch == ord('l'):
            self.ball_up_corr -= np.ones([3], dtype=np.int_)

    def setup_template(self):
        template = np.zeros([2 * self.BALL_TEMPLATE_SIZE, 2 * self.BALL_TEMPLATE_SIZE], np.uint8)
        cv2.circle(template, (self.BALL_TEMPLATE_SIZE, self.BALL_TEMPLATE_SIZE), self.BALL_TEMPLATE_SIZE,
                   (255, 255, 255), -1)
        im2, circle_contours, hierarchy = cv2.findContours(template, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        self.ball_template = circle_contours[0]

    def __init__(self):
        self.setup_template()

    def _check_ball_color_from_center(self, hsv):
        """
        For debug checking HSV color from "center" of playground
        :param hsv:
        :return:
        """
        center = (350, 230)
        cv2.circle(hsv, center, 5, (255, 0, 0), 2)
        cv2.putText(hsv, str(hsv[center[1], center[0]]), (200, 200), cv2.QT_FONT_BLACK, 0.5, (0, 0, 255))
        cv2.imshow("img", hsv)
        print(hsv[center[1], center[0]])

    def _prepare_image(self, image):
        hsv = cv2.cvtColor(image.copy(), cv2.COLOR_RGB2HSV)
        hsv = cv2.medianBlur(hsv, 5)
        return hsv

    def _get_threshold_mask(self, hsv):
        color_lower = self.ball_hsv_color - self.ball_low_corr
        color_upper = self.ball_hsv_color + self.ball_up_corr

        mask = cv2.inRange(hsv, color_lower, color_upper)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, None, iterations=3)  # erode->dilate

        return mask

    def detect(self, image):
        self.check_keyboard()

        hsv = self._prepare_image(image)
        mask = self._get_threshold_mask(hsv)
        mask_visual = Drawer(mask, "Mask", cv2.COLOR_GRAY2RGB)

        if DEBUG:
            mask_visual.draw_text(str(self.ball_low_corr) + "|" + str(self.ball_up_corr))

        best_circle = self._get_best_circle(mask, mask_visual)

        ball = models.Ball((-1, -1), 0)
        if best_circle is not None:
            ball = models.Ball(best_circle[0], best_circle[1])

        if DEBUG:
            mask_visual \
                .draw_model(ball) \
                .show()

        return ball

    def _get_best_circle(self, mask, mask_visual):
        min_match_error = np.inf
        best_circle = None

        im2, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        for cnt in contours:
            if DEBUG:
                mask_visual.draw_contour(cnt)

            if cnt.size < self.MIN_CONTOUR_SIZE:
                continue

            if DEBUG:
                mask_visual.draw_contour(cnt, (255, 0, 0))

            (x, y), radius = cv2.minEnclosingCircle(cnt)
            if radius < self.MIN_CONTOUR_RADIUS:
                continue

            center = (int(x), int(y))
            radius = int(radius)

            if DEBUG:
                mask_visual.draw_circle(center, radius)

            if len(contours) > 1:
                ret = cv2.matchShapes(cnt, self.ball_template, 1, 0.0)
                if ret < min_match_error:
                    min_match_error = ret
                    best_circle = (center, radius)
            else:
                best_circle = (center, radius)

        return best_circle
