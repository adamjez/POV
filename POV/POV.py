import cv2
import sys
import numpy
import core
import game
from drawer import Drawer

###################
# Run Information #
###################
#
# ./POV.py -i image_name.png // Loads and Analyze Image
# ./POV.py -v video_name.mp4 // Loads and Analyze video

####################
# Field Parameters #
####################
LeftTopCorner = (80, 25)  # Specifies corner for playground rectangle
RightBottomCorner = (770, 515)  # Specifies corner for playground rectangle

LinePositions = [105, 265, 425, 588]  # Specifies lines distance in pixels from left
LinesWidth = 40  # Width of line in pixels for line segmentations

LinesBelongs = [1, 2, 1, 2]  # Specifies who owns players on given line indexed from left to right
PlayersCount = [3, 3, 3, 3]  # Specifies players count on each line indexed from left to right

Player1Color = (180, 242, 140)  # Color of player 1 dummys in HSV
Player2Color = (221, 211, 27)  # Color of player 2 dummys in HSV

DistanceBetweenDummys = 145  # Specifies distance between dummys on lines
DummyHeight = 46
ColorTolerance = 40  # Tolerance for segmentation by color

options = {
    "BallHSV": [121, 193, 164],

    "GoalGates": [
        [(86, 211), (97, 341)],
        [(755, 208), (765, 340)]
    ],
}


def visualParameters(playground):
    cv2.rectangle(playground, LeftTopCorner, RightBottomCorner, (255, 0, 0))

    height, width, channels = playground.shape
    for point in LinePositions:
        cv2.line(playground, (LeftTopCorner[0] + point, 0), (LeftTopCorner[0] + point, height), (0, 0, 255))

    for gate in options["GoalGates"]:
        cv2.rectangle(playground, gate[0], gate[1], (0, 0, 255), 1)


def reset_to_start(vidFile, frame_counter, frames_count):
    if frame_counter == frames_count - 1:
        vidFile.set(cv2.CAP_PROP_POS_FRAMES, 0)
        return True

    return False


def processVideo(videoPath, is_looping):
    try:
        vidFile = cv2.VideoCapture(videoPath)
    except:
        print("problem opening input stream")
        sys.exit(1)

    if not vidFile.isOpened():
        print("capture stream not open")
        sys.exit(1)

    preproc = core.preprocessor(LeftTopCorner, RightBottomCorner)
    proc = core.processor(options, LinePositions, LinesWidth, Player1Color, Player2Color, ColorTolerance,
                          LinesBelongs, PlayersCount, DistanceBetweenDummys)

    fps = vidFile.get(cv2.CAP_PROP_FPS)
    nFrames = int(vidFile.get(cv2.CAP_PROP_FRAME_COUNT))
    print("frame number: %s" % nFrames)
    print("FPS value: %s" % fps)
    print("size: %d x %d" % (vidFile.get(cv2.CAP_PROP_FRAME_WIDTH), vidFile.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    print("looping: %r" % is_looping)
    currentGame = game.Game(fps, nFrames)

    frame_counter = 0
    currentTime = 0
    while vidFile.isOpened():  # note that we don't have to use frame number here, we could read from a live written file.
        ret, frame = vidFile.read()  # read first frame, and the return code of the function.
        if ret is False: break

        if frame_counter < 314:
            frame_counter += 1
            currentTime += int(1 / fps * 1000)
            continue

        if is_looping and reset_to_start(vidFile, frame_counter, nFrames):
            frame_counter = 0

        # visualParameters(frame)
        print("Current Time: " + str(currentTime))

        playground = preproc.run(frame)
        gameFrame = proc.run(playground)
        currentGame.processFrame(gameFrame)

        if space_hit(1):
            print("(x) Video paused")
            space_hit()
            print("(>) Video unpaused")

        if break_loop():
            break

        currentTime += int(1 / fps * 1000)  # in mSec
        frame_counter += 1

    vidFile.release()
    cv2.destroyAllWindows()


def space_hit(delay=None):
    if delay is None:
        ch = 0xFF & cv2.waitKey()
    else:
        ch = 0xFF & cv2.waitKey(delay)
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
    args_count = len(sys.argv)

    if args_count < 3:
        print("Incorrect number of parameters given")
        sys.exit(1)

    isLooping = args_count >= 4 and sys.argv[3] == "-l"
    inputType = sys.argv[1]

    if inputType == "-i":
        processImage(sys.argv[2])
    elif inputType == "-v":
        processVideo(sys.argv[2], isLooping)
    else:
        print("Unkown parameter given")
        sys.exit(1)
