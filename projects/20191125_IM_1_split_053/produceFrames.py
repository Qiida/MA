import os
from src.data.cam.Cam import Cam
import cv2 as cv

from src.utils.directories import CAM_DIR

if __name__ == '__main__':

    f = os.path.join(CAM_DIR, "20191125_IM_1_split_053_front.avi")
    cam = Cam(f)
    num = cam.getNumberOfFrames()

    for frameNr in range(num):
        imageFile = f"{frameNr:09d}.png"
        frame = cam.getNextFrameGray()
        cv.imwrite(imageFile, frame)
        print("{} / {} exported.".format(f"{frameNr:09d}", f"{num:09d}"))
