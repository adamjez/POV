class game(object):
    """Simulates the game and evaluates it"""
    def __init__(self, fps, frameCount):
        self.fps = fps
        self.frameCount = frameCount

    def processFrame(self, gameFrame):
        print("This is it")

class gameFrame(object):
    """Simulates the game and evaluates it"""
    def __init__(self, ball, players):
        self.ball = ball
        self.players = players
