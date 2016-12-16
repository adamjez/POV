import game
from detector.detect_ball import DetectBall
from detector.detect_goal import DetectGoal
from detector.detect_players import DetectPlayers
from detector.detect_ball_heatmap import DetectBallHeatMap


class processor:
    def __init__(self, options, fps):
        self.detect_players = DetectPlayers(options)
        self.detect_ball = DetectBall(options)
        self.detect_goal = DetectGoal(options)
        self.detect_ball_heatmap = DetectBallHeatMap(options, fps)

    def run(self, image):
        players = self.detect_players.detect(image)
        ball = self.detect_ball.detect(image)
        goal = self.detect_goal.detect(image, ball)
        heatmap = self.detect_ball_heatmap.detect(image, ball)

        return ball, players, image, goal, heatmap


class preprocessor:
    def __init__(self, play_ground):
        self.play_ground = play_ground

    def run(self, image):
        playground = image[
                     self.play_ground[0][1]:self.play_ground[1][1],
                     self.play_ground[0][0]:self.play_ground[1][0]].copy()
        return playground
