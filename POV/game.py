from drawer import Drawer


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

    def __init__(self, ball, players, image):
        self.ball = ball
        self.players = players
        self.image = image

        drawer = Drawer(image)

        drawer.draw_model(ball)

        for player in players:
            drawer.draw_model(player)

        drawer.show()
