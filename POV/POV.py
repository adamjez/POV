import cv2
import sys
import numpy
import core
import game

###################
# Run Information #
###################
#
# ./POV.py -i image_name.png // Loads and Analyze Image
# ./POV.py -v video_name.mp4 // Loads and Analyze video

####################
# Field Parameters #
####################
LeftTopCorner = (75, 14)  # Specifies corner for playground rectangle
RightBottomCorner = (770, 510)  # Specifies corner for playground rectangle

LinePositions = [100, 270, 430, 600]  # Specifies lines distance in pixels from left
LinesWidth = 40  # Width of line in pixels for line segmentations

LinesBelongs = [1, 2, 1, 2]  # Specifies who owns players on given line indexed from left to right
PlayersCount = [3, 3, 3, 3]  # Specifies players count on each line indexed from left to right

Player1Color = (180, 242, 140)  # Color of player 1 dummys in HSV
Player2Color = (221, 211, 27)  # Color of player 2 dummys in HSV

DistanceBetweenDummys = 145  # Specifies distance between dummys on lines
DummyHeight = 46
ColorTolerance = 40  # Tolerance for segmentation by color


def visualParameters(image):
    cv2.rectangle(image, LeftTopCorner, RightBottomCorner, (255, 0, 0))

    height, width, channels = image.shape
    for point in LinePositions:
        cv2.line(image, (LeftTopCorner[0] + point, 0), (LeftTopCorner[0] + point, height), (0, 0, 255))


def processVideo(videoPath):
    try:
        vidFile = cv2.VideoCapture(videoPath)
    except:
        print("problem opening input stream")
        sys.exit(1)

    if not vidFile.isOpened():
        print("capture stream not open")
        sys.exit(1)

    preproc = core.preprocessor(LeftTopCorner, RightBottomCorner)
    proc = core.processor(LinePositions, LinesWidth, Player1Color, Player2Color, ColorTolerance,
                          LinesBelongs, PlayersCount, DistanceBetweenDummys, DummyHeight)

    fps = vidFile.get(cv2.CAP_PROP_FPS)
    nFrames = int(vidFile.get(cv2.CAP_PROP_FRAME_COUNT))
    print("frame number: %s" % nFrames)
    print("FPS value: %s" % fps)
    print("size: %d x %d" % (vidFile.get(cv2.CAP_PROP_FRAME_WIDTH), vidFile.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    currentGame = game.Game(fps, nFrames)

    currentTime = 0
    for i in range(290):
        ret, frame = vidFile.read()  # read first frame, and the return code of the function.
        currentTime += int(1 / fps * 1000)
    
    while ret:  # note that we don't have to use frame number here, we could read from a live written file.
        # visualParameters(frame)
        # cv2.imshow("frameWindow", frame)
        # cv2.waitKey()
        print("Current Time: " + str(currentTime))

        #cv2.imshow("test", frame)
        #cv2.waitKey()
        playground = preproc.run(frame)
        gameFrame = proc.run(playground)
        currentGame.processFrame(gameFrame)

        if space_hit():
            print("(+) Video paused")
            while True:
                if space_hit():
                    print("(>) Video unpaused")
                    break

        if break_loop():
            break

        ret, frame = vidFile.read()
        currentTime += int(1 / fps * 1000)  # in mSec

    vidFile.release()
    cv2.destroyAllWindows()


def space_hit():
    ch = 0xFF & cv2.waitKey(1)
    if ch == 32:  # escape
        return True

    return False


def break_loop():
    ch = 0xFF & cv2.waitKey(1)
    if ch == 27:  # escape
        return True
    elif ch == ord('q'):
        return True
    return False


def processImage(imagePath):
    frame = cv2.imread(imagePath)

    preproc = core.preprocessor(LeftTopCorner, RightBottomCorner)
    proc = core.processor(LinePositions, LinesWidth, Player1Color, Player2Color, ColorTolerance,
                          LinesBelongs, PlayersCount, DistanceBetweenDummys)

    playground = preproc.run(frame)
    proc.run(playground)

    visualParameters(frame)
    cv2.imshow("frameWindow", frame)
    # cv2.waitKey(int(1/fps*1000)) # time to wait between frames, in mSec
    cv2.waitKey()


################
# MAIN PROGRAM #
################

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Incorrect number of parameters given")
        sys.exit(1)

    inputType = sys.argv[1]

    if inputType == "-i":
        processImage(sys.argv[2])
    elif inputType == "-v":
        processVideo(sys.argv[2])
    else:
        print("Unkown parameter given")
        sys.exit(1)
