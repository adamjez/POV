import numpy as np
import cv2


class DetectBallHeatMap:
    def __init__(self, options, fps):
        self.options = options
        self.inc_counter = np.ones(3) / fps
        self.heatmap = None

    def detect(self, image, ball):
        if self.heatmap is None:
            self.heatmap = np.zeros(image.shape)

        if ball.position == ball.INVALID_POSITION:
            return

        actual_frame = np.zeros(image.shape)
        cv2.circle(actual_frame, ball.position, ball.BALL_KNOWN_RADIUS, self.inc_counter, -1)
        self.heatmap += actual_frame

        return self.heatmap
