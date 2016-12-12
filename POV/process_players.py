import sys
import cv2
import numpy as np
from scipy.ndimage.filters import gaussian_filter
import matplotlib.pyplot as plt

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
        self.stripWidth = 75

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
                cv2.rectangle(image, (linePos - self.stripWidth, index - 5), (linePos + self.stripWidth, index + 5), (255, 0, 0))

                strip = image[index - 5: index + 5, linePos - self.stripWidth:linePos + self.stripWidth].copy()
                dummyStrips.append(strip)
                cv2.circle(image, (linePos, index), 5, (255, 0, 0), 10)
                #cv2.imshow("test", strip)
                #cv2.waitKey()
            #dummyStrips[0] = cv2.cvtColor(dummyStrips[0], cv2.COLOR_RGB2GRAY)

            (width, center) = self.computeDummyWidth(dummyStrips, currentPlayerColor)
            for index in dummyIndexes:
                dummys.append(models.Dummy((linePos, index), belongs, lineIndex, (linePos + center, index)))
                cv2.rectangle(image, (linePos + center - int(width/2), index - int(self.dummyHeight / 2)), (linePos + center + int(width/2), index + int(self.dummyHeight / 2)), (255, 0, 0))

            #cv2.imshow("Image", image)
            #cv2.waitKey()
            lineIndex += 1

        return dummys

    def computeDummyWidth(self, strips, playerColor):
        colorValues = []
        i = 0
        for strip in strips:
            gray = cv2.cvtColor(strip,cv2.COLOR_RGB2GRAY)
            ret,gray = cv2.threshold(gray,162,255,0)
            strips[i] = gray
            #strips[i] = cv2.cvtColor(strip, cv2.COLOR_RGB2HSV)
            i += 1

        playerColor = 255                         

        for i in range(self.stripWidth * 2):
            colorDiff = 0
            for j in range(10):
                for strip in strips:
                    colorDiff += abs(strip[j, i] - 255)
            colorValues.append(int(colorDiff))

        colorValues = gaussian_filter(colorValues, sigma=1)

        #colorValues = colorValues / np.max(colorValues)

        #plt.plot(range(0, len(colorValues)), colorValues)
        #plt.show()

        index = self.stripWidth
        i = 0
        for x in colorValues:
            # Magic constnat? Yes, change it if detection of feet doesn't work, but be carefoul it can damage your computer
            if x < 3000 and abs(i - self.stripWidth) >abs(index - self.stripWidth):
                index = i
            i += 1

        return (self.linesWidth, index - self.stripWidth)

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
