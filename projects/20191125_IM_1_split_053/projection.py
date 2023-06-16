import math
import os

import numpy as np

import pandas as pd

from src.app.CPointMatcher.CorrespondencePointMatcher import extractPointPairs
from src.data.lidar.LidarObjectFactory import getLidarObjects
from src.lcm.projection.Projector import Projector
from src.opencv.solvePNP.PnpSolver import PnpSolver
from src.utils.calibration import loadCalibration
from src.utils.directories import RESOURCES_DIR

import random

SEEDS = range(300)
NUMBER_OF_POINTS = range(10, 500)

lidarObjects = getLidarObjects("Export_pp_20191125_IM_1_split_053")
frames, imgPts, objPts = extractPointPairs(
    correspondencePointsFile="correspondences_full.txt",
    lidarObjects=lidarObjects
)
cameraMatrix, dist = loadCalibration(
    file=os.path.join(RESOURCES_DIR, "calibration", "calibration.txt"),
    verbose=True
)


def sampleFromList(lst: list, size: int, _seed: int):
    if size < 0 or size > len(lst):
        return None
    indices = list(range(len(lst)))
    random.seed(_seed)
    random.shuffle(indices)
    return indices[:size]


names = []
distance_means = []
diff_u_means = []
diff_v_means = []
seeds = []
number_of_points = []

number_of_cases = len(SEEDS) * len(NUMBER_OF_POINTS)
case = 0
for seed in SEEDS:
    for numberOfPoints in NUMBER_OF_POINTS:

        sample = sampleFromList(imgPts, numberOfPoints, seed)

        _frames, _imgPts, _objPts = [], [], []
        for i in sample:
            _frames.append(frames[i])
            _imgPts.append(imgPts[i])
            _objPts.append(objPts[i])

        solver = PnpSolver(_imgPts, _objPts, cameraMatrix, dist)
        projector = Projector(
            intrinsic=solver.intrinsic,
            extrinsic=solver.extrinsic,
            verbose=False
        )

        projectedPts = []
        for objPt in _objPts:
            projectedPts.append(
                projector.project(objPt)
            )

        diff_u, diff_v = [], []
        distance = []
        for i, projectedPt in enumerate(projectedPts):
            diff_u.append(np.abs(projectedPt[0] - _imgPts[i][0]))
            diff_v.append(np.abs(projectedPt[1] - _imgPts[i][1]))
            distance.append(math.sqrt(diff_u[i] * diff_u[i] + diff_v[i] * diff_v[i]))

        dictionary = {
            "frame": _frames,
            "objectPoints": _objPts,
            "imagePoints": _imgPts,
            "projectedPoints": projectedPts,
            "diff_u": diff_u,
            "diff_v": diff_v,
            "distance": distance
        }

        name = f"projection_s{seed}_n{numberOfPoints}"
        dataFrame = pd.DataFrame(dictionary)
        dataFrame.to_csv(
            os.path.join("csv", f"{name}.csv"), index=False
        )

        names.append(name)
        distance_means.append(np.mean(distance))
        diff_u_means.append(np.mean(diff_u))
        diff_v_means.append(np.mean(diff_v))
        seeds.append(seed)
        number_of_points.append(numberOfPoints)

        print(f"{case} / {number_of_cases}")
        case = case + 1



overviewDictionary = {
    "name": names,
    "distance_mean": distance_means,
    "diff_u_mean": diff_u_means,
    "diff_v_mean": diff_v_means,
    "seed": seeds,
    "numberOfPoints": number_of_points
}

overviewDataFrame = pd.DataFrame(overviewDictionary)
overviewDataFrame.to_csv(
    os.path.join("csv", f"overview.csv"), index=False
)

print("The End.")
