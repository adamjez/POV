class Ball(object):
    """Represents ball in playground"""
    def __init__(self, position, width, height):
        self.position = position
        self.width = width
        self.height = height

class Dummy(object):
    """Represents dummy (footbal player) on the line"""
    def __init__(self, position, playerIndex, lineIndex):
        self.position = position
        self.playerIndex = playerIndex
        self.lineIndex = lineIndex


