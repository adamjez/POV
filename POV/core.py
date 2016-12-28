from detector.detect_ball import DetectBall
from detector.detect_ball_heatmap import DetectBallHeatMap
from detector.detect_goal import DetectGoal
from detector.detect_players import DetectPlayers
from detector.detect_touch import DetectTouch


class processor:
    def __init__(self, options, fps):
        self.detect_players = DetectPlayers(options)
        self.detect_ball = DetectBall(options)
        self.detect_goal = DetectGoal(options)
        self.detect_ball_heatmap = DetectBallHeatMap(options, fps)
        self.detect_touch = DetectTouch(options)
        self.play_ground = options['PlayGround']

    def preprocess(self, image):
        playground = image[
                     self.play_ground[0][1]:self.play_ground[1][1],
                     self.play_ground[0][0]:self.play_ground[1][0]].copy()
        return playground

    def run(self, image):
        players = self.detect_players.detect(image)
        ball = self.detect_ball.detect(image)
        heatmap = self.detect_ball_heatmap.detect(image, ball)
        touch = self.detect_touch.detect(players, ball)
        goal = self.detect_goal.detect(image, ball)

        return ball, players, image, goal, heatmap, touch
