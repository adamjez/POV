import numpy as np


class DetectTouch:
    def __init__(self, options):
        self.options = options["Touch"]
        self.detectionTolerance = self.options["ToleranceDetection"]
        self.lastPlayerTouch = None

    def euklidien_distance(self, position1, position2):
        return np.sqrt((position1[0] - position2[0]) ** 2 + (position1[1] - position2[1]) ** 2)

    def detect(self, players, ball):
        ballPosition = ball.get_position()
        if ballPosition[0] < 0 or ballPosition[1] < 0:
            return None
         
        playersWithDistance = [(self.euklidien_distance(player.get_foot_position(), ballPosition), player) for player in players]
        closestPlayers = sorted(playersWithDistance, key=lambda player: player[0])

        if len(closestPlayers) == 0:
            return None

        closestPlayer = closestPlayers[0]
        if closestPlayer[0] < self.detectionTolerance and self.lastPlayerIdtouch != closestPlayer[1].get_player_index():
            self.lastPlayerIdtouch = closestPlayer[1].get_player_index()
            return closestPlayer[1]

        return None
