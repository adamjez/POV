import sys
import cv2
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

options = {
    "PlayGround": (
        (80, 25),  # Specifies corner for playground rectangle
        (770, 515)  # Specifies corner for playground rectangle
    ),

    'Lines': {
        'XPos': [105, 265, 425, 588],  # Specifies lines distance in pixels from left
        'Width': 40,  # Width of line in pixels for line segmentations
        'Belongs': [1, 2, 1, 2]  # Specifies who owns players on given line indexed from left to right
    },

    'Players': {
        'Count': [3, 3, 3, 3],  # Specifies players count on each line indexed from left to right
        'Player1Color': (180, 242, 140),  # Color of player 1 dummys in HSV
        'Player2Color': (221, 211, 27)  # Color of player 2 dummys in HSV
    },

    'Dummy': {
        'FeetDetectionTolerance': 1700,  # Bigger value more feet detection with more false alarams
        'DistanceBetween': 145,  # Specifies distance between dummys on lines
        'Height': 40,
        'ColorTolerance': 40,  # Tolerance for segmentation by color
        'Strip': (75, 10)
    },

    'Ball': {
        'HSV': [121, 193, 164],
        'MinContourSize': 10,
        'MinRadius': 9,
    },

    "Goals": {
        "HistoryLength": 5,
        "Gates": (
            [(0, 193), (15, 313)],
            [(675, 190), (690, 310)]
        )
    },

    "Touch": {
        "ToleranceDetection": 34
    },
}


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

    fps = vidFile.get(cv2.CAP_PROP_FPS)
    nFrames = int(vidFile.get(cv2.CAP_PROP_FRAME_COUNT))
    print("frame number: %s" % nFrames)
    print("FPS value: %s" % fps)
    print("size: %d x %d" % (vidFile.get(cv2.CAP_PROP_FRAME_WIDTH), vidFile.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    print("looping: %r" % is_looping)

    preproc = core.preprocessor(options['PlayGround'])
    proc = core.processor(options, fps)
    currentGame = game.Game(options, fps, nFrames)

    frame_counter = 0
    currentTime = 0

    # nFrames = 460 # TODO put away

    while vidFile.isOpened():  # note that we don't have to use frame number here, we could read from a live written file.
        ret, frame = vidFile.read()  # read first frame, and the return code of the function.
        if ret is False: break

        # if frame_counter < 300:
        #     frame_counter += 1
        #     currentTime += int(1 / fps * 1000)
        #     continue

        if is_looping and reset_to_start(vidFile, frame_counter, nFrames):
            frame_counter = 0

        playground = preproc.run(frame)
        ball, players, image, goal, heatmap, touch = proc.run(playground)
        currentGame.processFrame(currentTime, frame_counter, ball, players, image, goal, heatmap, touch)

        break_type = key_detected()
        if break_type is True:
            break

        currentTime += int(1 / fps * 1000)  # in mSec
        frame_counter += 1

    currentGame.gameEnd()
    vidFile.release()
    cv2.destroyAllWindows()


def key_detected():
    ch = 0xFF & cv2.waitKey(1)
    if ch == 32:  # escape
        print("(x) Video paused")
        while True:
            ch = 0xFF & cv2.waitKey(1)
            if ch == 32:  # escape
                break

        print("(>) Video unpaused")
        return False
    elif ch == 27:  # escape
        return True
    elif ch == ord('q'):
        return True
    return False


def processImage(imagePath):
    frame = cv2.imread(imagePath)

    preproc = core.preprocessor(options['PlayGround'])
    proc = core.processor(options)

    playground = preproc.run(frame)
    proc.run(playground)

    # visualParameters(frame)
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
        try:
            processVideo(sys.argv[2], isLooping)
        except KeyboardInterrupt:
            pass
        finally:
            print("TODO show_some_analysis")
    else:
        print("Unkown parameter given")
        sys.exit(1)
