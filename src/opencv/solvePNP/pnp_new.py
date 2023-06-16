import os
import numpy as np
import cv2 as cv

from src.app.CPointMatcher.CorrespondencePointMatcher import extractPointPairs
from src.data.lidar.LidarObjectFactory import getLidarObjects
from src.utils.calibration import loadCalibration
from src.utils.directories import RESOURCES_DIR

lidarObjects = getLidarObjects("Export_pp_20191125_IM_1_split_053")
imagePoints, objectPoints = extractPointPairs(correspondencePointsFile="correspondences.txt", lidarObjects=lidarObjects)


imagePoints = np.array(imagePoints)
objectPoints = np.array(objectPoints)
print(imagePoints)
print(objectPoints)

cameraMatrix, dist = loadCalibration(os.path.join(RESOURCES_DIR, "calibration", "calibration_rect.txt"), True)
rvec = np.array([0, 0, 0], dtype=np.float64, )
rvec.shape = (3, 1)
tvec = np.array([2.22, 0, 1.7], dtype=np.float64)
tvec.shape = (3, 1)

ret, rvec, tvec = cv.solvePnP(
    objectPoints=objectPoints,
    imagePoints=imagePoints,
    cameraMatrix=cameraMatrix,
    distCoeffs=dist,
    rvec=rvec,
    tvec=tvec,
    useExtrinsicGuess=True,
    flags=cv.SOLVEPNP_ITERATIVE
)

if ret:
    print(rvec)
    print(tvec)
    np.savez("pnp_result", rvec=rvec, tvec=tvec)

rmat = np.zeros((3, 3))

cv.Rodrigues(rvec, rmat)
extrinsic = np.hstack((np.transpose(rmat), tvec))
np.savez("extrinsic_iterative_autoPoints_71.npz", extrinsic=extrinsic)
