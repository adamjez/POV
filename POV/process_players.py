import sys
import cv2
import numpy as np
from scipy.ndimage.filters import gaussian_filter

import models


class ProcessPlayers:
    def __init__(self, linesPosition, linesWidth, player1Color, player2Color, tolerance, lineBelongs, playersCount,
                 distanceBetweenDummys):
        self.linesPosition = linesPosition
        self.linesWidth = linesWidth
        self.player1Color = player1Color
        self.player2Color = player2Color
        self.tolerance = tolerance
        self.lineBelongs = lineBelongs
        self.playersCount = playersCount
        self.distanceBetweenDummys = distanceBetweenDummys
        self.dummyHeight = 40

    def detect(self, image):
        height, width, channels = image.shape
        return self.processLines(image, height)

    def processLines(self, image, height):
        dummys = []
        lineIndex = 0
        for linePos, belongs, playersCount in zip(self.linesPosition, self.lineBelongs, self.playersCount):
            sourceSegment = image[0:height, linePos - int(self.linesWidth/2):linePos + int(self.linesWidth/2)].copy()

            currentPlayerColor = self.player1Color if belongs == 1 else self.player2Color
            dummyIndexes = self.segmentLines(sourceSegment.copy(), 
                                             currentPlayerColor, 
                                             playersCount,
                                             True if lineIndex % 3 == 0 else False)

            dummyStrips = []
            for index in dummyIndexes:
                strip = image[index - 5: index + 5, linePos - 60:linePos + 60].copy()
                dummyStrips.append(strip)
                cv2.circle(image, (linePos, index), 5, (255, 0, 0), 10)
                #cv2.imshow("test", strip)
                #cv2.waitKey()

            (width, center) = self.computeDummyWidth(dummyStrips, currentPlayerColor)
            for index in dummyIndexes:
                dummys.append(models.Dummy((linePos, index), belongs, lineIndex))
                cv2.rectangle(image, (linePos + center - int(width/2), index - int(self.dummyHeight / 2)), (linePos + center + int(width/2), index + int(self.dummyHeight / 2)), (255, 0, 0))

            #cv2.imshow("Image", image)
            #cv2.waitKey()
            lineIndex += 1

        #cv2.imshow("Image", image)
        #cv2.waitKey()

        return dummys

    def computeDummyWidth(self, strips, playerColor):
        colorValues = []
        color = (99, 44)
        strips[0] = cv2.cvtColor(strips[0], cv2.COLOR_RGB2HSV)
        strips[1] = cv2.cvtColor(strips[1], cv2.COLOR_RGB2HSV)
        playerColor = playerColor if playerColor == self.player1Color else (110,  90, 161)
        #playerColor = (120, 242, 140)
        #cv2.imshow("test1", strips[0])
        #cv2.imshow("test2", strips[1])
        #cv2.waitKey()
        for i in range(120):
            colorDiff = 0
            for j in range(10):
                colorDiff += abs(strips[0][j, i][1] - playerColor[1]) + abs(strips[1][j, i][1] - playerColor[1]) 
                + abs(strips[0][j, i][0] - playerColor[0]) + abs(strips[1][j, i][0] - playerColor[0])
                + (abs(strips[0][j, i][2] - playerColor[2]) + abs(strips[1][j, i][2] - playerColor[2])) / 2
            colorValues.append(colorDiff)

        colorValues = colorValues / np.max(colorValues)
        colorValues = gaussian_filter(colorValues, sigma=2, mode='nearest')

        #plt.plot(range(0, len(colorValues)), colorValues)

        index = colorValues.argmin(axis=0)
        colorValues[self.normalize(index - 16, 120):self.normalize(index + 16, 120)] = sys.maxsize
        index2 = colorValues.argmin(axis=0)
        #plt.plot(range(0, len(colorValues)), colorValues)
        #plt.show()

        if colorValues[index2] < 0.4:
            # we got two indexes
            mainIndex = index if abs(index - 60) < abs(index2 - 60) else index2
            minorIndex = index2 if mainIndex == index else index

            center = int((minorIndex - 60) * 1.3)
            width = 40
            return (width, center)

        return (self.linesWidth, 0)

    def segmentLines(self, image, color, playersCount, computeLastMiddlePlayer):
        rows = self.compueMeanSquareForEachRow(cv2.cvtColor(image, cv2.COLOR_RGB2HSV), color)

        rows = gaussian_filter(rows, sigma=11, mode='nearest')

        frameHeight = len(rows)
        #plt.plot(range(0, frameHeight), rows)
        #plt.show()

        rowIndexes = []

        distanceBetweenDummys = self.distanceBetweenDummys
        if computeLastMiddlePlayer:
            playersCount -= 1
            distanceBetweenDummys = distanceBetweenDummys * 2

        firstIndex = self.findNMinims(rows, playersCount, distanceBetweenDummys)
        for playerIndex in range(playersCount):
            index = firstIndex + playerIndex * distanceBetweenDummys
            rowIndexes.append(index)

        # try hill climbing for even better results
        i = 0
        for rowIndex in rowIndexes:
            rowIndexes[i] = self.hillClimbing(rowIndex, rows)
            i += 1

        if computeLastMiddlePlayer and len(rowIndexes) == 2:
            # if we got atleast 2 players and they are on the sides we can get middle one
            # If distance between these 2 players is greater then distance between dummys and magic constant so we can find middle one
            index = int((rowIndexes[0] + rowIndexes[1]) / 2)
            rowIndexes.append(index)

        return rowIndexes

    def hillClimbing(self, startingIndex, rows):
        currentIndex = startingIndex;
        maxIndex = len(rows)
        while True:
            L = self.neighbors(currentIndex, maxIndex);
            nextEval = np.inf;
            nextIndex = None;
            for x in L: 
                if rows[x] < nextEval:
                    nextIndex = x;
                    nextEval = rows[x];
            if nextEval >= rows[currentIndex]:
                #Return current node since no better neighbors exist
                return currentIndex;
            currentIndex = nextIndex

    def neighbors(self, index, maxIndex):
        if index == 0:
            return [index + 1]
        elif index == maxIndex:
            return [index - 1]
        return [index + 1, index - 1]

    def findNMinims(self, rows, playersCount, distanceBetweenDummys):
        rowsCount = len(rows)
        lastMaxIndex = (playersCount - 1) * distanceBetweenDummys

        minIndex = -1
        minValue = sys.maxsize
        while lastMaxIndex < rowsCount:
            sum = 0
            for i in range(playersCount):
                sum += rows[lastMaxIndex - i * distanceBetweenDummys]
            if sum < minValue:
                minIndex = lastMaxIndex - (playersCount - 1) * distanceBetweenDummys
                minValue = sum
            lastMaxIndex += 1

        return minIndex

    def normalize(self, index, frameHeight):
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
            rowSum = rowSum ** (1 / 2.0)

            rows.append(int(rowSum))

        return rows
