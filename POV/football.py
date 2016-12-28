import cv2
import sys
import core
import game


class Football:
    def __init__(self, options):
        self.options = options
        self.proc = None
        self.current_game = None

    @staticmethod
    def _get_capture_info(vidFile, is_looping):
        frames_count = int(vidFile.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = vidFile.get(cv2.CAP_PROP_FPS)
        width = vidFile.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = vidFile.get(cv2.CAP_PROP_FRAME_HEIGHT)

        print("frame number: %s" % frames_count)
        print("FPS value: %s" % fps)
        print("size: %d x %d" % (width, height))
        print("looping: %r" % is_looping)

        return frames_count, fps, width, height

    def processVideo(self, videoPath, is_looping, min_frame=None, max_frame=None):
        try:
            try:
                vidFile = cv2.VideoCapture(videoPath)
            except:
                print("problem opening input stream")
                sys.exit(1)

            if not vidFile.isOpened():
                print("capture stream not open")
                sys.exit(1)

            frames_count, fps, _, _ = self._get_capture_info(vidFile, is_looping)

            self.proc = core.processor(self.options, fps)
            self.current_game = game.Game(self.options, videoPath, fps, frames_count)

            frame_counter = 0
            currentTime = 0

            if max_frame is not None:
                frames_count = max_frame

            while vidFile.isOpened():  # note that we don't have to use frame number here, we could read from a live written file.
                ret, frame = vidFile.read()  # read first frame, and the return code of the function.
                if ret is False: break

                if min_frame is not None and frame_counter < min_frame:
                    frame_counter += 1
                    currentTime += int(1 / fps * 1000)
                    continue

                if is_looping and self.reset_to_start(vidFile, frame_counter, frames_count):
                    frame_counter = 0

                self._process_frame(frame, frame_counter, currentTime)

                break_type = self.key_detected()
                if break_type is True:
                    break

                currentTime += int(1 / fps * 1000)  # in mSec
                frame_counter += 1

            self.current_game.gameEnd()
            vidFile.release()
            cv2.destroyAllWindows()
        except KeyboardInterrupt:
            pass

    def _process_frame(self, frame, frame_number, current_time):
        """
        Process one frame
        :param frame:
        :param frame_number:
        :param current_time:
        :return:
        """
        playground = self.proc.preprocess(frame)
        ball, players, image, goal, heatmap, touch = self.proc.run(playground)
        self.current_game.processFrame(current_time, frame_number, ball, players, image, goal, heatmap, touch)

    def processImage(self, image_path: str):
        """
        Process image as one frame of video
        :param image_path: should be same as one video frame
        :return: None
        """
        frame = cv2.imread(image_path)
        self.proc = core.processor(self.options, 1)
        self.current_game = game.Game(self.options, image_path, 1, 1)
        self._process_frame(frame, 0, 0)
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
