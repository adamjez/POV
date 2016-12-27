import numpy as np
import os

from drawer import Drawer
from event_logger import EventLogger
from resultCheck import resultCheck


class Game(object):
    """Simulates the game and evaluates it"""

    def __init__(self, options, videoName, fps, frameCount):
        self.options = options
        self.fps = fps
        self.frameCount = frameCount
        self.score = [0, 0]
        self.touchBuffer = []
        filename, file_extension = os.path.splitext(videoName)
        self.resultLog = filename + "_result.txt"
        self.correctLog = filename + ".txt"
        self.eventLogger = EventLogger(self.resultLog)
        self.shooter_index = None

    def processFrame(self, currentTime, frameNumber, ball, players, image, goal, heatmap, touch):
        output = Drawer(image)
        output.draw_model(ball)

        output.draw_rect(self.options['Goals']['Gates'][0])
        output.draw_rect(self.options['Goals']['Gates'][1])

        for player in players:
            output.draw_model(player)

        if np.any(goal):
            shooterIndex = self.touchBuffer[0].get_player_index()
            # TODO calculate which index it is may be better
            self.shooter_index = shooterIndex[0] * self.options['Players']['Count'][0] + shooterIndex[1] - 1
            self.eventLogger.addGoal(currentTime, 1 if goal[0] else 2)

        if self.shooter_index is not None:
            output.draw_circle(players[self.shooter_index].get_position(), 20)

        self.score = np.add(self.score, goal)

        output.draw_text(str(self.score[0]), (295, 0), size=2)
        output.draw_text(str(self.score[1]), (355, 0), size=2)

        width, height, depth = image.shape

        output.draw_text("{0:.2f}s".format(currentTime / 1000) + "|" + str(frameNumber), (0, height - 290),
                         size=0.6)

        height, width, channels = image.shape
        self._draw_lines(output, height)

        # if heatmap is not None:
        #     Drawer(heatmap, "Ball heat map").show()

        if touch is not None:
            output.draw_circle(touch.get_position(), 40, (0, 255, 255), 5)
            self.eventLogger.addTouch(currentTime, touch)
            self.touchBuffer.insert(0, touch)
            if len(self.touchBuffer) > self.options['Touch']['BufferSize']:
                self.touchBuffer.pop()

        for i, touch in enumerate(self.touchBuffer):
            output.draw_text("TOUCH - playerId: " + str(touch.get_player_index()), (0, i * 16), size=0.6)

        output.show()

    def _draw_lines(self, output: Drawer, height) -> Drawer:
        for point in self.options['Lines']['XPos']:
            output.draw_line((point, 0), (point, height))
        return output

    def gameEnd(self):
        self.eventLogger.save()

        rc = resultCheck(self.correctLog, self.resultLog)
        rc.run()
        rc.printResult()
