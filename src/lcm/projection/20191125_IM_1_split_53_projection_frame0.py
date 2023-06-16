import os
from os.path import join

import matplotlib
import numpy as np

from src.data.cam.Cam import Cam
from src.data.lidar.LidarObjectFactory import getLidarObjects
from src.utils.calibration import loadCalibration
from src.utils.directories import RESOURCES_DIR, ROOT_DIR, CAM_DIR

matplotlib.use("TkAgg")

import cv2 as cv

intrinsic, _ = loadCalibration(os.path.join(RESOURCES_DIR, "calibration", "calibration_rect.txt"))
intrinsic_matrix = np.zeros((3, 4))
for i in range(3):
    for j in range(4):
        try:
            intrinsic_matrix[i][j] = intrinsic[i][j]
        except IndexError:
            pass
        # TODO: Das geht besser

print(intrinsic_matrix)
# extrinsic = np.load(join(ROOT_DIR, "src", "opencv", "solvePNP", "extrinsic_ransac_ippe_1035.npz")).get("extrinsic")
# extrinsic = np.load(join(ROOT_DIR, "src", "opencv", "solvePNP", "extrinsic_sqpnp_1035.npz")).get("extrinsic")
extrinsic = np.load(join(ROOT_DIR, "src", "opencv", "solvePNP", "extrinsic_IPPE_autoPoints_71.npz")).get("extrinsic")

# print(extrinsic)

extrinsic_matrix = np.zeros((4, 4))

for i in range(3):
    for j in range(3):
        try:
            extrinsic_matrix[i][j] = extrinsic[i][j]
        except IndexError:
            pass
        # TODO: Das geht besser
extrinsic_matrix[0][3] = extrinsic[0][3]
extrinsic_matrix[1][3] = extrinsic[1][3]
extrinsic_matrix[2][3] = extrinsic[2][3]
extrinsic_matrix[3][3] = 1

a = np.zeros((3, 4))
a[0][0] = 1
a[1][1] = 1
a[2][2] = 1

print(extrinsic_matrix)

lidarObjects = getLidarObjects("Export_pp_20191125_IM_1_split_053")

bb10 = lidarObjects[10].boundingBox
imgPts10 = bb10.getTransformedImagePoints(0, intrinsic, extrinsic)

bb8 = lidarObjects[8].boundingBox
imgPts8 = bb8.getTransformedImagePoints(0, intrinsic, extrinsic)

bb5 = lidarObjects[5].boundingBox
imgPts5 = bb5.getTransformedImagePoints(0, intrinsic, extrinsic)
f = join(CAM_DIR, "20191125_IM_1_split_053_front.avi")
cam = Cam(file=f)
img = cam.getNextFrame()
img_rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)

print(imgPts10)
print(imgPts8)
print(imgPts5)


def drawProjectedBoundingBox(imagePoints):
    cv.line(img_rgb,
            (int(imagePoints[0][0]),
             int(imagePoints[0][1])),
            (int(imagePoints[1][0]),
             int(imagePoints[1][1])),
            bb10.color,
            2)
    cv.line(img_rgb,
            (int(imagePoints[1][0]),
             int(imagePoints[1][1])),
            (int(imagePoints[2][0]),
             int(imagePoints[2][1])),
            bb10.color,
            2)
    cv.line(img_rgb,
            (int(imagePoints[2][0]),
             int(imagePoints[2][1])),
            (int(imagePoints[3][0]),
             int(imagePoints[3][1])),
            bb10.color,
            2)
    cv.line(img_rgb,
            (int(imagePoints[3][0]),
             int(imagePoints[3][1])),
            (int(imagePoints[0][0]),
             int(imagePoints[0][1])),
            bb10.color,
            2)


drawProjectedBoundingBox(imgPts10)
drawProjectedBoundingBox(imgPts8)
drawProjectedBoundingBox(imgPts5)

cv.imshow("yea", img_rgb)
cv.waitKey(0)

# cv2.destroyAllWindows() simply destroys all the windows we created.
cv.destroyAllWindows()
