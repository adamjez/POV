import cv2
from abc import ABC, abstractmethod


class BaseModel(ABC):
    @abstractmethod
    def __init__(self, position):
        self.position = position

    @abstractmethod
    def render(self, image):
        pass


class Ball(BaseModel):
    """Represents ball in playground"""

    def render(self, image):
        cv2.rectangle(image, self.position, (self.position[0] + 2, self.position[1] + 2), (255, 0, 0), 3)
        cv2.circle(image, self.position, self.radius, (0, 255, 0), 2)

    def __init__(self, position, radius):
        super().__init__(position)
        self.radius = radius


class Dummy(BaseModel):
    """Represents dummy (footbal player) on the line"""

    def render(self, image):
        cv2.rectangle(image, self.position, (self.position[0] + 3, self.position[1] + 3), (255, 0, 0), 3)

    def __init__(self, position, playerIndex, lineIndex):
        super().__init__(position)
        self.playerIndex = playerIndex
        self.lineIndex = lineIndex
