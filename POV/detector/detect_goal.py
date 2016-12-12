from drawer import Drawer
import cv2
import numpy as np


class DetectGoal:
    def __init__(self, options):
        self.goal_gates = options["GoalGates"]

    def detect(self, image, ball):
        goal_keep_mask = np.zeros([image.shape[0], image.shape[1]], np.uint8)
        ball_mask = goal_keep_mask.copy()

        left_top = (0, 195)
        left_bottom = (0, 312)

        right_top = (668, 190)
        right_bottom = (680, 310)

        # left goal keep
        cv2.rectangle(goal_keep_mask, left_top, left_bottom, (255, 255, 255), thickness=-1)
        # right goal keep
        cv2.rectangle(goal_keep_mask, right_top, right_bottom, (255, 255, 255), thickness=-1)

        cv2.circle(ball_mask, ball.position, ball.BALL_KNOWN_RADIUS, (255, 255, 255), -1)
        ball_contour = cv2.findNonZero(ball_mask)
        ball_leftmost = tuple(ball_contour[ball_contour[:, :, 0].argmin()][0])
        ball_rightmost = tuple(ball_contour[ball_contour[:, :, 0].argmax()][0])

        # mask = np.zeros(image.shape)
        Drawer(image) \
            .draw_rect(left_top, left_bottom) \
            .draw_rect(right_top, right_bottom) \
            .draw_marker(ball_leftmost, color=(0, 0, 255)) \
            .draw_marker(ball_rightmost, color=(0, 0, 255))\
            # .show()

        if goal_keep_mask[ball_leftmost[1], ball_leftmost[0]] == 255:
            print("RIGHT SCORES")
            return [False, True]

        if goal_keep_mask[ball_rightmost[1], ball_rightmost[0]] == 255:
            print("LEFT SCORES")
            return [True, False]

        return [False, False]
