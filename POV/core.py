import cv2
import numpy

class processor:

    def __init__(self, linesPosition, linesWidth):
        self.linesPosition = linesPosition
        self.linesWidth = linesWidth
        self.time = 0.0

    def run(self, image):
        height, width, channels = image.shape
        self.processLines(image, height)


    def processLines(self, image, height):
        linesSegment = []
        for linePos in self.linesPosition:
            lineSegment = image[0:height, linePos - int(self.linesWidth/2):linePos + int(self.linesWidth/2)].copy()
            linesSegment.append(lineSegment)

            cv2.imshow("LineSegment", lineSegment)
            cv2.waitKey()

class preprocessor:
    
    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2

    def run(self, image):
        playground = image[self.point1[1]:self.point2[1], self.point1[0]:self.point2[0]].copy()
        return playground
