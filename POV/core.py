import game
from processor.process_ball import ProcessBall
from processor.process_players import ProcessPlayers


class processor:
    def __init__(self, options, linesPosition, linesWidth, player1Color, player2Color, tolerance, lineBelongs, playersCount,
                 distanceBetweenDummys):
        self.process_ball = ProcessBall(options)
        self.process_players = ProcessPlayers(linesPosition, linesWidth, player1Color, player2Color, tolerance,
                                              lineBelongs, playersCount, distanceBetweenDummys)

    def run(self, image):
        players = self.process_players.detect(image)
        ball = self.process_ball.detect(image)
        return game.GameFrame(ball, players, image)


class preprocessor:
    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2

    def run(self, image):
        playground = image[self.point1[1]:self.point2[1], self.point1[0]:self.point2[0]].copy()
        return playground
