import math
import os

import numpy as np
import pandas
import pandas as pd

from src.app.CPointMatcher.CorrespondencePointMatcher import extractPointPairs
from src.data.lidar.LidarObjectFactory import getLidarObjects
from src.lcm.projection.Projector import Projector
from src.opencv.solvePNP.PnpSolver import PnpSolver
from src.utils.calibration import loadCalibration
from src.utils.directories import RESOURCES_DIR

import random

SEED = 27
N = 188

lidarObjects = getLidarObjects("Export_pp_20191125_IM_1_split_053")

imgPts, objPts = extractPointPairs(
    correspondencePointsFile="correspondences_full.txt",
    lidarObjects=lidarObjects
)
cameraMatrix, dist = loadCalibration(
    file=os.path.join(RESOURCES_DIR, "calibration", "calibration_rect.txt"),
    verbose=True
)


def sampleFromList(lst: list, size: int, _seed: int):
    if size < 0 or size > len(lst):
        return None
    indices = list(range(len(lst)))
    random.seed(_seed)
    random.shuffle(indices)
    return indices[:size]


sample = sampleFromList(imgPts, N, SEED)

_imgPts, _objPts = [], []
for i in sample:
    _imgPts.append(imgPts[i])
    _objPts.append(objPts[i])

solver = PnpSolver(_imgPts, _objPts, cameraMatrix, dist)
projector = Projector(
    intrinsic=solver.intrinsic,
    extrinsic=solver.extrinsic,
    verbose=True
)

projectedPts = []

corners = lidarObjects[10].boundingBox.getCornersFromIdNr(0)
for corner in corners:
    projectedPts.append(
        projector.project(corner)
    )


print("The End.")
