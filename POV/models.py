import cv2
from abc import ABC, abstractmethod


class BaseModel(ABC):
    INVALID_POSITION = (-1, -1)

    @abstractmethod
    def __init__(self, position):
        self.position = position

    @abstractmethod
    def render_model(self, image):
        pass

    def render(self, image):
        """
        Do not override this
        :param image:
        :return:
        """
        if self.position == self.INVALID_POSITION: return
        self.render_model(image)


class Ball(BaseModel):
    BALL_KNOWN_RADIUS = 22
    """Represents ball in playground"""

    def render_model(self, image):
        cv2.rectangle(image, self.position, (self.position[0] + 2, self.position[1] + 2), (255, 0, 0), 3)
        cv2.circle(image, self.position, self.radius, (0, 200, 0), 1)
        cv2.circle(image, self.position, self.BALL_KNOWN_RADIUS, (0, 255, 0), 2)

    def __init__(self, position, radius):
        super().__init__(position)
        self.radius = radius


class Dummy(BaseModel):
    """Represents dummy (footbal player) on the line"""

    def render_model(self, image):
        cv2.rectangle(image, self.position, (self.position[0] + 3, self.position[1] + 3), (255, 0, 0), 3)

    def __init__(self, position, playerIndex, lineIndex, footPosition, player):
        super().__init__(position)
        self.playerIndex = playerIndex
        self.lineIndex = lineIndex
        self.footPosition = footPosition
        self.player = player
