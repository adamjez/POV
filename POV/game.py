from drawer import Drawer
import numpy as np
import cv2
from ring_buffer import RingBuffer

class Game(object):
    """Simulates the game and evaluates it"""

    def __init__(self, options, fps, frameCount):
        self.options = options
        self.fps = fps
        self.frameCount = frameCount
        self.score = [0, 0]
        self.touchBuffer = []

    def processFrame(self, currentTime, frameNumber, ball, players, image, goal, heatmap, touch):
        output = Drawer(image)
        output.draw_model(ball)

        output.draw_rect(self.options['Goals']['Gates'][0])
        output.draw_rect(self.options['Goals']['Gates'][1])

        for player in players:
            output.draw_model(player)

        self.score = np.add(self.score, goal)

        output.draw_text(str(self.score[0]), (295, 0), size=2)
        output.draw_text(str(self.score[1]), (355, 0), size=2)

        width, height, depth = image.shape

        output.draw_text("{0:.2f}".format(currentTime / 1000) + "|" + str(frameNumber), (0, height - 290), size=0.6)

        # height, width, channels = image.shape
        # for point in LinePositions:
        #     cv2.line(playground, (options['PlayGround'][0][0] + point, 0),
        #              (options['PlayGround'][0][0] + point, height), (0, 0, 255))

        if heatmap is not None:
            Drawer(heatmap, "Ball heat map").show()

        if touch is not None and touch[0]:
            self.touchBuffer.insert(0, touch[1])
            if len(self.touchBuffer) > 5:
                self.touchBuffer.pop()

        for i, touch in enumerate(self.touchBuffer):
            output.draw_text("TOUCH - playerId: " + str(touch), (0, i * 16), size=0.6)

        output.show()
