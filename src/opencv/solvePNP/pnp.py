from os.path import join

from src.data.TestVehicle import TestVehicle
from src.lcm.LidarCameraMapper import LidarCameraMapper

import numpy as np
import cv2 as cv

from src.opencv.solvePNP.IM_1_split_053_imgPoints import imagePoints
from src.utils import LIDAR_DIR, CAM_DIR

lcm = LidarCameraMapper(testVehicle=TestVehicle("TEASY3"),
                        matFile=join(LIDAR_DIR, "Export_pp_20191125_IM_1_split_053.mat"),
                        camFile=join(CAM_DIR, "20191125_IM_1_split_053_front.avi"))

cameraParams = np.load("../calibration/CameraParams.npz")

cameraMatrix = cameraParams.get("cameraMatrix")
dist = cameraParams.get("dist")
# rvecs = cameraParams.get("rvecs")
# tvecs = cameraParams.get("tvecs")


imagePoints
objectPoints = []


v10 = lcm.lidarObjects[10].boundingBox.getCornersFromIdNr(0)
objectPoints.append((v10[2][0], v10[2][1], v10[2][2]))
objectPoints.append((v10[1][0], v10[1][1], v10[1][2]))
v8 = lcm.lidarObjects[8].boundingBox.getCornersFromIdNr(0)
objectPoints.append((v8[0][0], v8[0][1], v8[0][2]))
objectPoints.append((v8[2][0], v8[2][1], v8[2][2]))
objectPoints.append((v8[3][0], v8[3][1], v8[3][2]))
v5 = lcm.lidarObjects[5].boundingBox.getCornersFromIdNr(0)
objectPoints.append((v5[0][0], v5[0][1], v5[0][2]))
objectPoints.append((v5[2][0], v5[2][1], v5[2][2]))
objectPoints.append((v5[3][0], v5[3][1], v5[3][2]))

objectPoints = np.array(objectPoints)
print(objectPoints)

# ret, rvec, tvec = cv.solvePnP(objectPoints, imagePoints, cameraMatrix, dist, useExtrinsicGuess=False, flags=cv.SOLVEPNP_IPPE)
cameraMatrix[0][0] = 780.9496109
cameraMatrix[1][1] = 782.48266718
cameraMatrix[0][2] = 388.97613468
cameraMatrix[1][2] = 275.93810157
dist[0][0] = 0.12471368
dist[0][1] = 0.19934625
dist[0][2] = 0
dist[0][3] = 0
dist[0][4] = 0
ret, rvec, tvec = cv.solvePnP(objectPoints, imagePoints, cameraMatrix, dist)
if ret:
    print(rvec)
    print(tvec)
    np.savez("pnp_result", rvec=rvec, tvec=tvec)
print("wow")

rmat = np.zeros((3, 3))

cv.Rodrigues(rvec, rmat)
extrinsic = np.hstack((np.transpose(rmat), tvec))
np.savez("extrinsic_old", extrinsic=extrinsic)

