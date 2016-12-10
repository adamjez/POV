class Game(object):
    """Simulates the game and evaluates it"""

    def __init__(self, fps, frameCount):
        self.fps = fps
        self.frameCount = frameCount

    def processFrame(self, gameFrame):
        pass
        # print("This is it")
        # TODO


class GameFrame(object):
    """Simulates the game and evaluates it"""

    def __init__(self, ball, players):
        self.ball = ball
        self.players = players
