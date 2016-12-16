import numpy as np
import cv2


class DetectBallHeatMap:
    def __init__(self, options):
        self.options = options
        self.heatmap = None

    def detect(self, image, ball):
        if self.heatmap is None:
            self.heatmap = np.zeros(image.shape)

        if ball.position == ball.INVALID_POSITION: return

        # cv2.circle(self.heatmap, ball.position, ball.BALL_KNOWN_RADIUS, (255, 255, 255), -1)

        self.heatmap[ball.position[1]:ball.position[1] + 10, ball.position[0]:ball.position[0] + 10] += (1, 1, 1)

        cv2.imshow("map", self.heatmap)
