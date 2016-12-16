import numpy as np
import cv2


class DetectBallHeatMap:
    def __init__(self, options):
        self.options = options
        self.heatmap = None

    def detect(self, image, ball):
        if self.heatmap is None:
            self.heatmap = np.zeros(image.shape)

        if ball.position == ball.INVALID_POSITION:
            return

        actual_frame = np.zeros(image.shape)
        cv2.circle(actual_frame, ball.position, ball.BALL_KNOWN_RADIUS, (0.1, 0.1, 0.1), -1)
        self.heatmap += actual_frame

        return self.heatmap