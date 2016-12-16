import game
from detector.detect_ball import DetectBall
from detector.detect_goal import DetectGoal
from detector.detect_players import DetectPlayers


class processor:
    def __init__(self, options, linesPosition, linesWidth, player1Color, player2Color, tolerance, lineBelongs,
                 playersCount,
                 distanceBetweenDummys):
        self.detect_players = DetectPlayers(linesPosition, linesWidth, player1Color, player2Color, tolerance,
                                            lineBelongs, playersCount, distanceBetweenDummys)
        self.detect_ball = DetectBall(options)
        self.detect_goal = DetectGoal(options)

    def run(self, image):
        # TODO do we need the copy? or how we're gonna handle writing to output (some output_frame?)
        players = self.detect_players.detect(image.copy())
        ball = self.detect_ball.detect(image)
        goal = self.detect_goal.detect(image, ball)
        return game.GameFrame(ball, players, image, goal)


class preprocessor:
    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2

    def run(self, image):
        playground = image[self.point1[1]:self.point2[1], self.point1[0]:self.point2[0]].copy()
        return playground
