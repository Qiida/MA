from os.path import join, isfile

import cv2 as cv
import matplotlib

from src.utils.directories import CAM_DIR

matplotlib.use("TkAgg")


class Cam:

    def __init__(self, file=None):

        # Public.
        self.file = None

        # Private.
        self.capture = None
        self.__initialize(file)

    def __initialize(self, file):
        self.file = file

        if self.file is not None:
            self.read()

    def read(self, file=None):
        if file is not None:
            if isfile(file):
                self.file = file
        self.capture = cv.VideoCapture(self.file)

        if self.capture.isOpened():
            print("{} was successfully captured.".format(self.file))

    def getFPS(self):
        if self.hasVideoCapture:
            return int(self.capture.get(cv.CAP_PROP_FPS))

    def getNextFrame(self):
        success, frame = self.capture.read()
        if success:
            rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            return rgb
        else:
            return None

    def getNextFrameGray(self):
        success, frame = self.capture.read()
        if success:
            gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

            return gray
        else:
            return None

    def getCapture(self):
        return self.capture

    def plotNextFrame(self, axis):
        nextFrame = self.getNextFrame()
        if nextFrame is not None:
            axis.imshow(nextFrame)

    def getWidth(self):
        if self.hasVideoCapture:
            width = self.capture.get(cv.CAP_PROP_FRAME_WIDTH)
            return int(width)

    def getHeight(self):
        if self.hasVideoCapture:
            height = self.capture.get(cv.CAP_PROP_FRAME_HEIGHT)
            return int(height)

    def getNumberOfFrames(self):
        if self.hasVideoCapture():
            frameCount = self.capture.get(cv.CAP_PROP_FRAME_COUNT)
            return int(frameCount)

    def hasVideoCapture(self):
        return self.capture is not None

    def buildAxis(self, figure):
        rect = [0.1, 0.1, 0.8, 0.8]
        return figure.add_axes(rect=rect)

    def release(self):
        self.capture.release()



if __name__ == '__main__':

    f = join(CAM_DIR, "20191125_IM_1_split_053_front.avi")
    cam = Cam(file=f)

    print("FPS: {}".format(cam.getFPS()))
    print("Width: {}, Height: {}".format(cam.getWidth(), cam.getHeight()))
    print("Frames: {}".format(cam.getNumberOfFrames()))

    for frameNr in range(cam.getNumberOfFrames()):
        frame = cam.getNextFrame()
        cv.imwrite(f"{frameNr:09d}.png", frame)

    # h, w = frame.shape[:2]
    # # newCameraMatrix, roi = cv.getOptimalNewCameraMatrix(intrinsics)
    # # rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    # plt.imshow(frame)
    # plt.show()
