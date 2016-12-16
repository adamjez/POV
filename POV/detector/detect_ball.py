import cv2
import numpy as np
import models
from drawer import Drawer

DEBUG = False


class DetectBall:
    def create_template(self):
        size = models.Ball.BALL_KNOWN_RADIUS
        template = np.zeros([2 * size, 2 * size], np.uint8)
        cv2.circle(template, (size, size), size,
                   (255, 255, 255), -1)
        im2, circle_contours, hierarchy = cv2.findContours(template, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        return circle_contours[0]

    def __init__(self, options):
        self.ball_options = options['Ball']
        self.ball_hsv_color = self.ball_options['HSV']
        self.ball_low_corr = np.array([50, 50, 50])  # TODO maybe tweak the corrections
        self.ball_up_corr = np.array([20, 20, 20])
        self.ball_template = self.create_template()

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
        hsv = cv2.medianBlur(hsv, 5)  # TODO might not be necessary
        return hsv

    def _get_threshold_mask(self, hsv):
        color_lower = self.ball_hsv_color - self.ball_low_corr
        color_upper = self.ball_hsv_color + self.ball_up_corr

        mask = cv2.inRange(hsv, color_lower, color_upper)
        # mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, None, iterations=3)  # erode->dilate

        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))

        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=3)  # erode->dilate

        return mask

    def detect(self, image):
        # self.check_keyboard()

        hsv = self._prepare_image(image)

        mask = self._get_threshold_mask(hsv)
        mask_visual = Drawer(mask, "Mask", cv2.COLOR_GRAY2RGB)

        if DEBUG:
            mask_visual.draw_text(str(self.ball_low_corr) + "|" + str(self.ball_up_corr))

        best_circle, best_contour = self._get_best_circle(mask, mask_visual)

        if best_circle is not None:
            ball = models.Ball(best_circle[0], best_circle[1], best_contour)
        else:
            ball = models.Ball(models.BaseModel.INVALID_POSITION, 0, None)

        if DEBUG:
            mask_visual \
                .draw_model(ball) \
                .show()

        return ball

    def _get_best_circle(self, mask, mask_visual):
        min_match_error = np.inf
        best_ball = None
        best_contour = None

        im2, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        for cnt in contours:
            if DEBUG:
                mask_visual.draw_contour(cnt)

            if cnt.size < self.ball_options['MinContourSize']:
                continue

            # TODO better filtering (based on this? http://layer0.authentise.com/detecting-circular-shapes-using-contours.html )

            if DEBUG:
                mask_visual.draw_contour(cnt, (255, 0, 0))

            (x, y), radius = cv2.minEnclosingCircle(cnt)
            if radius < self.ball_options['MinRadius']:
                continue

            center = (int(x), int(y))
            radius = int(radius)

            if DEBUG:
                mask_visual.draw_circle(center, radius)

            if len(contours) > 1:
                ret = cv2.matchShapes(cnt, self.ball_template, 1, 0.0)
                if ret < min_match_error:
                    min_match_error = ret
                    best_ball = (center, radius)
                    best_contour = cnt
            else:
                best_ball = (center, radius)
                best_contour = cnt

        return best_ball, best_contour
