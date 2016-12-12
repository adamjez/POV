import cv2

class Ball(object):
    """Represents ball in playground"""
    def __init__(self, position, radius):
        self.position = position
        self.radius = radius

    def render(self, image):
        cv2.circle(image, self.position, self.radius, (0, 255, 0), 2)


class Dummy(object):
    """Represents dummy (footbal player) on the line"""
    def __init__(self, position, playerIndex, lineIndex):
        self.position = position
        self.playerIndex = playerIndex
        self.lineIndex = lineIndex


