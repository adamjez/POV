import cv2
import numpy as np

from ring_buffer import RingBuffer


class DetectGoal:
    _HISTORY_LENGTH = 5

    def __init__(self, options):
        self.options = options["Goals"]

        self.ball_in_field_history = RingBuffer(self.options['HistoryLength'])
        self.ball_in_left_goal_history = RingBuffer(2 * self.options['HistoryLength'])
        self.ball_in_right_goal_history = RingBuffer(2 * self.options['HistoryLength'])

    def detect(self, image, ball):
        goal_keep_mask = np.zeros([image.shape[0], image.shape[1]], np.uint8)
        height, width, channels = image.shape

        # left goal keep
        left = self.options['Gates'][0]
        cv2.rectangle(goal_keep_mask, tuple(left[0]), tuple(left[1]), (255, 255, 255), thickness=-1)
        # right goal keep
        right = self.options['Gates'][1]
        cv2.rectangle(goal_keep_mask, tuple(right[0]), tuple(right[1]), (255, 255, 255), thickness=-1)

        ball_boundaries = ball.get_boundaries(width)
        self.ball_in_field_history.extend(np.array(ball.is_visible()))
        self.ball_in_left_goal_history.extend(goal_keep_mask[ball_boundaries[0][1], ball_boundaries[0][0]] == 255)
        self.ball_in_right_goal_history.extend(goal_keep_mask[ball_boundaries[1][1], ball_boundaries[1][0]] == 255)

        if self._detect_goal(self.ball_in_left_goal_history):
            return [False, True]
        elif self._detect_goal(self.ball_in_right_goal_history):
            return [True, False]
        else:
            return [False, False]

    def _detect_goal(self, ball_in_goal_area_history):
        """
        Checks goal within goal area and within history of frames
        :param ball_in_goal_area_history:
        :return: whether goal was detected
        """

        if np.any(ball_in_goal_area_history.get()) and not np.any(self.ball_in_field_history.get()):
            ball_in_goal_area_history.clear()
            return True
        return False
