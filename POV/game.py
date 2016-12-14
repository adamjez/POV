from drawer import Drawer
import numpy as np


class Game(object):
    """Simulates the game and evaluates it"""

    def __init__(self, fps, frameCount):
        self.fps = fps
        self.frameCount = frameCount
        self.score = [0, 0]

    def processFrame(self, gameFrame, currentTime):
        output = Drawer(gameFrame.image)
        output.draw_model(gameFrame.ball)

        for player in gameFrame.players:
            output.draw_model(player)

        # if gameFrame.goal_right:
        #     self.score[1] += 1

        self.score = np.add(self.score, gameFrame.goal)

        output.draw_text(str(self.score[0]), (295, 0), size=2)
        output.draw_text(str(self.score[1]), (355, 0), size=2)

        width, height, depth = gameFrame.image.shape

        output.draw_text(str(currentTime / 1000), (0, height - 290), size=0.6)

        output.show()


class GameFrame(object):
    """Simulates the game and evaluates it"""

    def __init__(self, ball, players, image, goal):
        self.ball = ball
        self.players = players
        self.image = image
        self.goal = goal
