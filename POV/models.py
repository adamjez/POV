import cv2
from abc import ABC, abstractmethod
import numpy as np


class BaseModel(ABC):
    INVALID_POSITION = (-1, -1)

    @abstractmethod
    def __init__(self, position):
        self.position = position

    @abstractmethod
    def render_model(self, drawer):
        pass

    def render(self, drawer):
        """
        Do not override this
        :param image:
        :return:
        """
        if self.position == self.INVALID_POSITION: return
        self.render_model(drawer)

    def is_visible(self):
        return self.position != self.INVALID_POSITION

    def get_position(self):
        return self.position


class Ball(BaseModel):
    """
    Represents ball in playground
    """
    BALL_KNOWN_RADIUS = 22

    def render_model(self, drawer):
        drawer.draw_rect((self.position, (self.position[0] + 2, self.position[1] + 2)), (255, 0, 0), 3)
        drawer.draw_circle(self.position, self.radius, (0, 200, 0), 1)
        drawer.draw_circle(self.position, self.BALL_KNOWN_RADIUS, (0, 255, 0), 2)

    def __init__(self, position, radius, contour):
        super().__init__(position)
        self.radius = radius
        self.contour = contour

    def __str__(self):
        return "(" + str(self.position) + " , " + str(self.BALL_KNOWN_RADIUS) + ")"

    def get_boundaries(self, img_width: int) -> tuple:
        """
        Returns left and rightmost points of known ball.
        If exceeds image size, returns max or min value
        :param img_width: playground width
        :return: (leftmost, rightmost)
        """
        leftmost = self.position[0] - self.BALL_KNOWN_RADIUS
        rightmost = self.position[0] + self.BALL_KNOWN_RADIUS

        return (
            (0 if leftmost < 0 else leftmost, self.position[1]),
            (img_width - 1 if rightmost >= img_width else rightmost, self.position[1])
        )


class Dummy(BaseModel):
    """Represents dummy (footbal player) on the line"""

    def render_model(self, drawer):
        drawer.draw_marker(self.footPosition, (0, 255, 0))
        drawer.draw_circle(self.position, 5, (0, 255, 0), -1)

    def __init__(self, position, playerIndex, lineIndex, footPosition, player):
        super().__init__(position)
        self.playerIndex = playerIndex
        self.lineIndex = lineIndex
        self.footPosition = footPosition
        self.player = player

    def get_foot_position(self):
        return self.footPosition

    def get_player_index(self):
        return self.playerIndex

    def __eq__(self, other):
        if other is not Dummy:
            return False
        else:
            return self.playerIndex == other.playerIndex
