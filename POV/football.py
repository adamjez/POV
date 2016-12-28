import cv2
import sys
import core
import game


class Football:
    def __init__(self, options):
        self.options = options

    def processVideo(self, videoPath, is_looping):
        try:
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

            proc = core.processor(self.options, fps)
            currentGame = game.Game(self.options, videoPath, fps, nFrames)

            frame_counter = 0
            currentTime = 0

            # nFrames = 460 # TODO put away

            while vidFile.isOpened():  # note that we don't have to use frame number here, we could read from a live written file.
                ret, frame = vidFile.read()  # read first frame, and the return code of the function.
                if ret is False: break

                # if frame_counter < 700:
                #     frame_counter += 1
                #     currentTime += int(1 / fps * 1000)
                #     continue

                if is_looping and self.reset_to_start(vidFile, frame_counter, nFrames):
                    frame_counter = 0

                playground = proc.preprocess(frame)
                ball, players, image, goal, heatmap, touch = proc.run(playground)
                currentGame.processFrame(currentTime, frame_counter, ball, players, image, goal, heatmap, touch)

                break_type = self.key_detected()
                if break_type is True:
                    break

                currentTime += int(1 / fps * 1000)  # in mSec
                frame_counter += 1

            currentGame.gameEnd()
            vidFile.release()
            cv2.destroyAllWindows()
        except KeyboardInterrupt:
            pass

    def processImage(self, imagePath):
        frame = cv2.imread(imagePath)

        proc = core.processor(self.options, 1)

        playground = proc.preprocess(frame)
        proc.run(playground)

        # visualParameters(frame)
        cv2.imshow("frameWindow", frame)
        # cv2.waitKey(int(1/fps*1000)) # time to wait between frames, in mSec
        cv2.waitKey()

    @staticmethod
    def reset_to_start(vidFile, frame_counter, frames_count):
        if frame_counter == frames_count - 1:
            vidFile.set(cv2.CAP_PROP_POS_FRAMES, 0)
            return True

        return False

    @staticmethod
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
