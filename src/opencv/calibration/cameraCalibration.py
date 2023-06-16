from os.path import join

import numpy as np
import cv2 as cv
import glob

from src.data.cam.Cam import Cam
from src.utils import CALIBRATION_DIR, CAM_DIR

# matplotlib.use("TkAgg")

# TODO: Fails with actual size.
# chessboardSize = (9, 6)
chessboardSize = (9, 5)  # Lose potential here. Switching from python 3.10 to 3.9 did not fix.
# chessboardSize = (5, 9)
f = join(CAM_DIR, "20191125_IM_1_split_050_back.avi")
cam = Cam(file=f)

print("FPS: {}".format(cam.getFPS()))
print("Width: {}, Height: {}".format(cam.getWidth(), cam.getHeight()))
print("Frames: {}".format(cam.getNumberOfFrames()))
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.0001)
frameSize = (800, 600)
objp = np.zeros((chessboardSize[0] * chessboardSize[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:chessboardSize[0], 0:chessboardSize[1]].T.reshape(-1, 2)

objPoints = []
imgPoints = []

images = glob.glob(CALIBRATION_DIR + "//*.png")

imgCounter = 0
for image in images:
    print(image)
    img = cv.imread(image)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    ret, corners = cv.findChessboardCorners(gray, chessboardSize, None)


    if ret:

        objPoints.append(objp)
        corners2 = cv.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        imgPoints.append(corners)

        cv.drawChessboardCorners(img, chessboardSize, corners2, ret)
        cv.imshow("img", img)

        cv.waitKey(1000)

        cv.imwrite("{}.jpg".format(imgCounter), img)
        imgCounter += 1


cv.destroyAllWindows()

ret, cameraMatrix, dist, rvecs, tvecs = cv.calibrateCamera(objPoints, imgPoints, frameSize, None, None)
print("Camera Calibrated: ", ret)
print("\nCamera Matrix: \n", cameraMatrix)
print("\nDistortion Parameters: \n", dist)
print("\nRotation Vectors: \n", rvecs)
print("\nTranslation Vectors: \n", tvecs)

np.savez("CameraParams", cameraMatrix=cameraMatrix, dist=dist, rvecs=rvecs, tvecs=tvecs)
print("Camera Calibrated.")

