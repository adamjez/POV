import cv2
import numpy as np
import sys
import math
import random
import matplotlib.pyplot as plt
from scipy.ndimage.filters import gaussian_filter

import models
import game

class processor:

    def __init__(self, linesPosition, linesWidth, player1Color, player2Color, tolerance, lineBelongs, playersCount, distanceBetweenDummys):
        self.linesPosition = linesPosition
        self.linesWidth = linesWidth
        self.player1Color = player1Color
        self.player2Color = player2Color
        self.tolerance = tolerance
        self.lineBelongs = lineBelongs
        self.playersCount = playersCount
        self.distanceBetweenDummys = distanceBetweenDummys

    def run(self, image):
        height, width, channels = image.shape
        players = self.processLines(image, height)
        ball = self.processBall(image)

        return game.gameFrame(ball, players)

    def processBall(self, image):
        return models.Ball((0,0), 0, 0)
     
    def processLines(self, image, height):
        dummys = []
        lineIndex = 0
        for linePos, belongs, playersCount in zip(self.linesPosition, self.lineBelongs, self.playersCount):
            sourceSegment = image[0:height, linePos - int(self.linesWidth/2):linePos + int(self.linesWidth/2)].copy()

            dummyIndexes = self.segmentLinesFirstVersion(sourceSegment.copy(), self.player1Color if belongs == 1 else self.player2Color, playersCount)

            for rowIndex in dummyIndexes:
                dummys.append(models.Dummy((linePos, dummyIndexes), belongs, lineIndex))
            #lineSegment2 = self.segmentLinesSecondVersion(sourceSegment.copy(), self.player1Color if belongs == 1 else self.player2Color, playersCount)

            lineIndex += 1

        return dummys

    def segmentLinesFirstVersion(self, image, color, playersCount):
        rows = self.compueMeanSquareForEachRow(cv2.cvtColor(image, cv2.COLOR_RGB2HSV), color)
        
        rows = gaussian_filter(rows, sigma=9, mode='nearest')

        frameHeight = len(rows)
        plt.plot(range(0, frameHeight), rows)
        plt.show()

        rowIndexes = []
        for playerIndex in range(playersCount):
            # if we got atleast 2 players and they are on the sides we can get middle one
            # If distance between these 2 players is greater then distance between dummys and magic constant so we can find middle one
            if playersCount == 3 and len(rowIndexes) == 2 and abs(rowIndexes[0] - rowIndexes[1]) > (self.distanceBetweenDummys * 1.6):
                index = int((rowIndexes[0] + rowIndexes[1]) / 2)
            else:
                index = rows.argmin(axis=0)

            rowIndexes.append(index)
            rows[self.normalizeToFrameHeight(index - self.distanceBetweenDummys, frameHeight):
                 self.normalizeToFrameHeight(index + self.distanceBetweenDummys, frameHeight)] = sys.maxsize
            cv2.circle(image, (int(self.linesWidth/2), index), 5, (255, 0, 0), 10)
        

        cv2.imshow("LineSegment", image)
        cv2.waitKey()

        return rowIndexes

    def normalizeToFrameHeight(self, index, frameHeight):
        if index < 0:
            return 0
        if index >= frameHeight:
            return frameHeight
        return index

    def compueMeanSquareForEachRow(self, image, color):
        height, width, channels = image.shape

        rows = []
        for i in range(height):
            rowSum = 0
            for j in range(width):
                distance = abs(image[i, j] - color)
                value = (distance[0] + distance[1]) ** 2
                rowSum += value

            rowSum = rowSum / width
            rowSum = rowSum ** (1/2.0)

            rows.append(int(rowSum))

        return rows


    def segmentLinesSecondVersion(self, image, color, playersCount):
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


class preprocessor:
    
    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2

    def run(self, image):
        playground = image[self.point1[1]:self.point2[1], self.point1[0]:self.point2[0]].copy()
        return playground
