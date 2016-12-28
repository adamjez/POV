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
        self.filename = filename
        self.resultLog = filename + "_result.txt"
        self.correctLog = filename + ".txt"
        self.eventLogger = EventLogger(self.resultLog)
        self.shooter_index = None

    def _calculate_player_index(self, shooter_index: list) -> int:
        return shooter_index[0] * self.options['Players']['Count'][0] + shooter_index[1] - 1

    def _log_goal(self, goal, currentTime):
        shooterIndex = self.touchBuffer[0].get_player_index()
        self.shooter_index = self._calculate_player_index(shooterIndex)
        self.eventLogger.addGoal(currentTime, 1 if goal[0] else 2)

    def processFrame(self, currentTime, frameNumber, ball, players, image, goal, heatmap, touch):
        output = Drawer(image, self.filename)
        output.draw_model(ball)

        for player in players:
            output.draw_model(player)

        if np.any(goal):
            self._log_goal(goal, currentTime)

        if self.shooter_index is not None:
            output.draw_circle(players[self.shooter_index].get_position(), 20)

        self.score = np.add(self.score, goal)

        if touch is not None:
            output.draw_circle(touch.get_position(), 40, (0, 255, 255), 5)
            self.eventLogger.addTouch(currentTime, touch)
            self.touchBuffer.insert(0, touch)
            if len(self.touchBuffer) > self.options['Touch']['BufferSize']:
                self.touchBuffer.pop()

        height, width, channels = image.shape
        self._draw(output, height, currentTime, frameNumber)
        output.show()

    def _draw(self, output: Drawer, height, currentTime, frameNumber):
        # goal gates
        output.draw_rect(self.options['Goals']['Gates'][0])
        output.draw_rect(self.options['Goals']['Gates'][1])
        # score
        output.draw_text(str(self.score[0]), (self.options['Goals']['ScoreXPos'][0], 0), size=2)
        output.draw_text(str(self.score[1]), (self.options['Goals']['ScoreXPos'][1], 0), size=2)
        # lines
        for point in self.options['Lines']['XPos']:
            output.draw_line((point, 0), (point, height))
        # cap info
        output.draw_text("{0:.2f}s".format(currentTime / 1000) + "|" + str(frameNumber), (0, height - 90), size=0.6)
        # touch events
        for i, touch in enumerate(self.touchBuffer):
            output.draw_text("TOUCH - playerId: " + str(touch.get_player_index()), (0, i * 17 - 40), size=0.6)

    def gameEnd(self):
        self.eventLogger.save()

        rc = resultCheck(self.correctLog, self.resultLog)
        rc.run()
        rc.printResult()
