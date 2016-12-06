import cv2
import numpy as np
import sys
import math
import random
import matplotlib.pyplot as plt
from scipy.ndimage.filters import gaussian_filter

class processor:

    def __init__(self, linesPosition, linesWidth, player1Color, player2Color, tolerance, lineBelongs, playersCount):
        self.linesPosition = linesPosition
        self.linesWidth = linesWidth
        self.player1Color = player1Color
        self.player2Color = player2Color
        self.tolerance = tolerance
        self.lineBelongs = lineBelongs
        self.playersCount = playersCount
        self.time = 0.0

    def run(self, image):
        height, width, channels = image.shape
        self.processLines(image, height)


    def processLines(self, image, height):
        linesSegment = []

        for linePos, belongs, playersCount in zip(self.linesPosition, self.lineBelongs, self.playersCount):
            sourceSegment = image[0:height, linePos - int(self.linesWidth/2):linePos + int(self.linesWidth/2)].copy()
            linesSegment.append(sourceSegment)

            lineSegment = self.segmentLines(sourceSegment.copy(), self.player1Color if belongs == 1 else self.player2Color, playersCount)

            cv2.imshow("LineSegment", lineSegment)
            cv2.waitKey()

            lineSegment2 = self.segmentLines2(sourceSegment.copy(), self.player1Color if belongs == 1 else self.player2Color, playersCount)

            cv2.imshow("LineSegment", lineSegment2)
            cv2.waitKey()

    def segmentLines(self, image, color, playersCount):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV);

        rows, min, index = self.compueMeanSquareForEachRow(image, color)
        
        rows = gaussian_filter(rows, sigma=10)

        plt.plot(range(0, 770), rows)
        plt.show()

        for index in range(playersCount):
            index = rows.argmin(axis=0)
            rows[index - 50:index + 50] = sys.maxsize
            cv2.circle(image, (50, index), 5, (255, 0, 0), 10)
        
        return image

    def segmentLines2(self, image, color, playersCount):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV);

        lower = np.array([c - self.tolerance for c in color])
        upper = np.array([c + self.tolerance for c in color])

        lower[2] = lower[2] - self.tolerance
        upper[2] = upper[2] + self.tolerance

        lineSegment = cv2.inRange(image, lower, upper)

        moments = cv2.moments(lineSegment)
        center = (int(moments['m10']/moments['m00']), int(moments['m01']/moments['m00']))
        cv2.circle(lineSegment, center, 3, self.player1Color, -1)

        return lineSegment

    def compueMeanSquareForEachRow(self, image, color):
        height, width, channels = image.shape

        rows = []
        min = sys.maxsize;
        index = -1
        for i in range(height):
            rowSum = 0
            for j in range(width):
                test = abs(image[i, j] - color)
                value = (test[0] + test[1]) ** 2
                rowSum += value

            rowSum = rowSum / width
            rowSum = rowSum ** (1/2.0)
            if rowSum < min:
                min = rowSum
                index = i
            rows.append(int(rowSum))

        return (rows, min, index)
        

class preprocessor:
    
    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2

    def run(self, image):
        playground = image[self.point1[1]:self.point2[1], self.point1[0]:self.point2[0]].copy()
        return playground
