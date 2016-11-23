import cv2
import sys
import numpy
import core

# Constants
First = (80, 30)
Second = (1480, 800)

LinePositions = [140, 300, 470, 650, 800, 970, 1150, 1320]
LinesWidth = 150

LinesBelongs = [1, 1, 2, 1, 2, 1, 2, 2]

PlayersCount = [1, 2, 3, 5, 5, 3, 2, 1]

Player1Color = (134, 240 ,180)
Player2Color = (0, 240, 180)

Tolerance = 40

def visualParameters(image):
    cv2.rectangle(image, First, Second, (255, 0, 0))

    height, width, channels = image.shape
    for point in LinePositions:
        cv2.line(image, (First[0] + point, 0), (First[0] + point, height), (0, 0, 255))


def loadFile():
    if len(sys.argv) < 2:
        print("first parameter have to be video file name")
        sys.exit(1)

    try:
        vidFile = cv2.VideoCapture(sys.argv[1])
    except:
        print("problem opening input stream")
        sys.exit(1)

    if not vidFile.isOpened():
        print("capture stream not open")
        sys.exit(1)

    nFrames = int(vidFile.get(cv2.CAP_PROP_FRAME_COUNT)) # one good way of namespacing legacy openCV: cv2.cv.*

    print("frame number: %s" %nFrames)
    fps = vidFile.get(cv2.CAP_PROP_FPS)
    print("FPS value: %s" %fps)

    preproc = core.preprocessor(First, Second)
    proc = core.processor(LinePositions, LinesWidth)

    ret, frame = vidFile.read() # read first frame, and the return code of the function.
    while ret:  # note that we don't have to use frame number here, we could read from a live written file.

        print("Drawing Frame")
        playground = preproc.run(frame)

        proc.run(playground)
        visualParameters(frame)
        cv2.imshow("frameWindow", frame)
        #cv2.waitKey(int(1/fps*1000)) # time to wait between frames, in mSec
        cv2.waitKey()
        cv2.imshow("frameWindow", playground)
        cv2.waitKey()

        ret, frame = vidFile.read() 
        ret = False

def loadImage():
    if len(sys.argv) < 2:
        print("first parameter have to be video file name")
        sys.exit(1)

    frame = cv2.imread(sys.argv[1])
    preproc = core.preprocessor(First, Second)
    proc = core.processor(LinePositions, LinesWidth, Player1Color, Player2Color, Tolerance,
                          LinesBelongs, PlayersCount)

    playground = preproc.run(frame)

    proc.run(playground)
    visualParameters(frame)
    cv2.imshow("frameWindow", frame)
    #cv2.waitKey(int(1/fps*1000)) # time to wait between frames, in mSec
    cv2.waitKey()
    
    #cv2.imshow("frameWindow", playground)
    #cv2.waitKey()

loadImage()