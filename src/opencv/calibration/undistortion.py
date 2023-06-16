from os.path import join

import cv2 as cv
import numpy as np

from src.data.TestVehicle import TestVehicle
from src.lcm.LidarCameraMapper import LidarCameraMapper
from src.utils.directories import LIDAR_DIR, CAM_DIR

lcm = LidarCameraMapper(testVehicle=TestVehicle("TEASY3"),
                        matFile=join(LIDAR_DIR, "Export_pp_20191125_IM_1_split_050.mat"),
                        camFile=join(CAM_DIR, "20191125_IM_1_split_050_back.avi"))

frameNr = 20
frame = lcm.buildFrame(frameNr=frameNr, frame=lcm.camFrames[frameNr])

cameraParams = np.load("CameraParams.npz")

cameraMatrix = cameraParams.get("cameraMatrix")
dist = cameraParams.get("dist")
rvecs = cameraParams.get("rvecs")
tvecs = cameraParams.get("tvecs")

cameraMatrix[0][0] = 780.9496109
cameraMatrix[1][1] = 782.48266718
cameraMatrix[0][2] = 388.97613468
cameraMatrix[1][2] = 275.93810157
cameraMatrix[2][2] = 1.
dist[0][0] = 0.12471368
dist[0][1] = 0.19934625
dist[0][2] = 0
dist[0][3] = 0
dist[0][4] = 0

img = cv.cvtColor(frame.image, cv.COLOR_BGR2RGB)
h, w = img.shape[:2]
newCameraMatrix, roi = cv.getOptimalNewCameraMatrix(cameraMatrix, dist, (w, h), 1, (w, h))

dst = cv.undistort(img, cameraMatrix, dist, None, newCameraMatrix)
x, y, w, h = roi
dst = dst[y:y+h, x:x+w]
cv.imwrite("caliResult.png", dst)

mapx, mapy = cv.initUndistortRectifyMap(cameraMatrix, dist, None, newCameraMatrix, (w,h), 5)
dst = cv.remap(img, mapx, mapy, cv.INTER_LINEAR)
x, y, w, h = roi
dst = dst[y:y+h, x:x+w]
cv.imwrite("caliResult2.png", dst)


