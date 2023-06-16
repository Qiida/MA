import os
from abc import ABC

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt


class EvaluationPlotter(ABC):
    def __init__(self, path, out, verbose=False, overlapThreshold=None):
        self.verbose = verbose
        self.path = path
        self.out = out
        self.overlapThreshold = overlapThreshold

        # public.

        self.figure = None
        self.axis = None
        self.objectTypes = None
        self.giantDataFrame = None
        self.boxes = None

        # private.
        self.__dataFrames = None
        self.__pathEndsWith = f"_COMBO_{overlapThreshold}.csv"

        self.__initialize()

    def __initialize(self):
        self.__initializeFigure()
        self.__buildDataFrames()
        self.__buildGiantDataFrame()
        self.__buildObjectTypes()
        self.__sortDistanceClasses()
        self.__sortMatched()

    def __initializeFigure(self):
        self.figure, self.axis = plt.subplots(1, 1, layout="constrained")

    def __buildDataFrames(self):
        self.__dataFrames = list()
        for file in os.listdir(self.path):
            if str(file).endswith(self.__pathEndsWith):
                self.__dataFrames.append(pd.read_csv(os.path.join(self.path, file), header=0))


    def __buildGiantDataFrame(self):
        self.giantDataFrame = pd.concat(self.__dataFrames, axis=0, ignore_index=False)

    def __buildObjectTypes(self):
        self.objectTypes = self.giantDataFrame.objectType.unique().tolist()
        if self.verbose:
            print(f"\n\n[objectTypes]\n{self.objectTypes}")

    def __sortMatched(self):
        overlaps = self.giantDataFrame.overlap.tolist()
        matched = []
        for overlap in overlaps:
            if not np.isnan(overlap):
                matched.append(True)
            else:
                matched.append(False)
        self.giantDataFrame = self.giantDataFrame.assign(matched=matched)

    def __sortDistanceClasses(self):
        distances = self.giantDataFrame.distance.tolist()
        distanceClasses = []
        for distance in distances:
            if 0 < distance < 10:
                distanceClasses.append(0)
            if 10 < distance < 20:
                distanceClasses.append(10)
            if 20 < distance < 30:
                distanceClasses.append(20)
            if 30 < distance < 40:
                distanceClasses.append(30)
            if 40 < distance < 50:
                distanceClasses.append(40)
            if 50 < distance < 60:
                distanceClasses.append(50)
            if 60 < distance < 70:
                distanceClasses.append(60)
            if 70 < distance < 80:
                distanceClasses.append(70)
            if 80 < distance < 90:
                distanceClasses.append(80)
            if 90 < distance:
                distanceClasses.append(90)
        self.giantDataFrame = self.giantDataFrame.assign(distanceClass=distanceClasses)

    def plotAndSave(self):
        pass
