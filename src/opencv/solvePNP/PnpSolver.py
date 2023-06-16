import os

import numpy as np
import cv2 as cv

from src.app.CPointMatcher.CorrespondencePointMatcher import extractPointPairs
from src.data.lidar.LidarObjectFactory import getLidarObjects
from src.utils.calibration import loadCalibration
from src.utils.directories import RESOURCES_DIR


class PnpSolver:
    def __init__(self, imagePoints, objectPoints, intrinsic, distortion, verbose=False):
        self.verbose = verbose
        self.imagePoints = imagePoints
        self.objectPoints = objectPoints

        self.intrinsic = intrinsic
        self.distortion = distortion
        self.extrinsic = None

        if len(imagePoints) == len(objectPoints):
            self.numberOfPoints = len(imagePoints)
            self.__initializeRvecTvec()
            self.__solve()
        else:
            print("imagePoints and objectPoints must be of same size.")

    def __solve(self):
        ret, self.rvec, self.tvec = cv.solvePnP(
            objectPoints=np.array(self.objectPoints),
            imagePoints=np.array(self.imagePoints),
            cameraMatrix=self.intrinsic,
            distCoeffs=self.distortion,
            rvec=self.rvec,
            tvec=self.tvec,
            useExtrinsicGuess=True,
            flags=cv.SOLVEPNP_ITERATIVE
        )
        if ret:
            if self.verbose:
                print(f"[rvec]\n{self.rvec}\n")
                print(f"[tvec]\n{self.tvec}")
        rmat = np.zeros((3, 3))
        cv.Rodrigues(self.rvec, rmat)
        self.extrinsic = np.hstack((np.transpose(rmat), self.tvec))

    def __initializeRvecTvec(self):
        self.rvec = np.array([0, 0, 0], dtype=np.float64, )
        self.rvec.shape = (3, 1)
        self.tvec = np.array([2.22, 0, 1.7], dtype=np.float64)
        self.tvec.shape = (3, 1)


if __name__ == '__main__':
    lidarObjects = getLidarObjects("Export_pp_20191125_IM_1_split_053")

    imgPts, objPts = extractPointPairs(
        correspondencePointsFile="correspondences.txt",
        lidarObjects=lidarObjects
    )
    cameraMatrix, dist = loadCalibration(
        file=os.path.join(RESOURCES_DIR, "calibration", "calibration_rect.txt"),
        verbose=True
    )

    solver = PnpSolver(imgPts, objPts, cameraMatrix, dist)
