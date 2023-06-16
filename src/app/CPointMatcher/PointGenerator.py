import math
import os
import json
import numpy as np
from abc import ABC

from matplotlib import pyplot as plt
from scipy import linalg
from scipy.signal import find_peaks

from src.utils.directories import PROJECTS_DIR


class AutoPoint(ABC):

    def __init__(self, file, verbose=False):
        self.verbose = verbose

        self.u = None
        self.v = None

        self.v_leveled = None
        self.maxima_i = None
        self.maxima, self.minima = [], []

        self.u_max = None
        self.u_max_i = None
        self.u_min = None
        self.u_min_i = None
        self.v_max = None
        self.v_max_i = None
        self.v_min = None
        self.v_min_i = None

        self.extractPoints(file)
        self.setGlobalMaximaMinima()

    def extractPoints(self, file):
        f = open(file)
        self.v = []
        self.u = []
        data = json.load(f)
        points = data["annotations"][0]["polygon"]["paths"][0]
        for point in points:
            self.u.append(point["x"])
            self.v.append(point["y"])

    def printGlobalMaxima(self):
        print("u_max: {}, i: {}".format(self.u_max, self.u_max_i))
        print("u_min: {}, i: {}".format(self.u_min, self.u_min_i))
        print("v_max: {}, i: {}".format(self.v_max, self.v_max_i))
        print("v_min: {}, i: {}".format(self.v_min, self.v_min_i))

    def setGlobalMaximaMinima(self):
        self.u_max = None
        self.u_max_i = None
        self.u_min = None
        self.u_min_i = None
        self.v_max = None
        self.v_max_i = None
        self.v_min = None
        self.v_min_i = None
        for i in range(len(self.u)):

            if self.u_max is None:
                self.__set_u_max(i)
                self.__set_u_min(i)

            if self.u_max < self.u[i]:
                self.__set_u_max(i)

            if self.u_min > self.u[i]:
                self.__set_u_min(i)

            if self.v_max is None:
                self.__set_v_max(i)
                self.__set_v_min(i)

            if self.v_max < self.v[i]:
                self.__set_v_max(i)

            if self.v_min > self.v[i]:
                self.__set_v_min(i)
        if self.verbose:
            self.printGlobalMaxima()

    def __set_u_max(self, i):
        self.u_max = self.u[i]
        self.u_max_i = i

    def __set_u_min(self, i):
        self.u_min = self.u[i]
        self.u_min_i = i

    def __set_v_max(self, i):
        self.v_max = self.v[i]
        self.v_max_i = i

    def __set_v_min(self, i):
        self.v_min = self.v[i]
        self.v_min_i = i

    def computeFittingV(self, *dims, right_vector):
        _left_matrix = self.__createLeftMatrix(*dims)
        _params = self.__computeBestFitParameters(_left_matrix, right_vector)
        _v_fit = _left_matrix @ _params
        return _v_fit.reshape(right_vector.shape)

    @staticmethod
    def __createLeftMatrix(*dims):
        _data = [dim.flatten() for dim in dims]
        _data.append(np.ones_like(_data[0]))
        return np.asarray(_data).transpose()

    @staticmethod
    def __computeBestFitParameters(left_matrix, right_vector):
        v_vector = right_vector.flatten()
        left_matrix_pseudo_inverse = linalg.pinv(left_matrix)
        return left_matrix_pseudo_inverse @ v_vector

    def plotAllPoints(self, axis, size=2, color="k"):
        axis.scatter(
            x=self.u,
            y=self.v,
            s=size,
            c=color
        )

    def plotLeveled(self, axis, size=2, color="c"):
        axis.scatter(
            x=self.u,
            y=self.v_leveled,
            s=size,
            c=color
        )


class FrontRightPoint(AutoPoint):
    def __init__(self, file, verbose=False):
        super(FrontRightPoint, self).__init__(
            file=file,
            verbose=verbose
        )

        self.maxima_i_filtered = []
        self.frontWheel, self.rearWheel = [], []

        self.coefficients = None
        self.wheelLine_u = None
        self.wheelLine_v = None
        self.imagePoint = None

        self.__computeMaximaIndexes()
        self.__filterMaxima()
        self.__setMaxima()
        self.__computeWheels()
        self.__computeCoefficients()
        self.__computeWheelLine()
        self.__computeImagePoint()

    def plotWheelLine(self, axis, lineWidth=0.2, color="c"):
        axis.plot(self.wheelLine_u, self.wheelLine_v, color=color, linewidth=lineWidth)

    def plotWheels(self, axis, size=10, color="r"):
        axis.scatter(self.frontWheel[0], self.frontWheel[1], size, color=color)
        axis.scatter(self.rearWheel[0], self.rearWheel[1], size, color=color)

    def printCoefficients(self):
        print("a =", self.coefficients[0])
        print("b =", self.coefficients[1])

    def __computeMaximaIndexes(self):
        v_fit = self.computeFittingV(np.array(self.u), right_vector=np.array(self.v))
        self.v_leveled = np.subtract(self.v, v_fit)
        self.maxima_i = find_peaks(self.v_leveled)

    def __computeCoefficients(self):
        wheels_u = [self.rearWheel[0], self.frontWheel[0]]
        wheels_v = [self.rearWheel[1], self.frontWheel[1]]
        self.coefficients = np.polyfit(wheels_u, wheels_v, 1)
        if self.verbose:
            self.printCoefficients()

    def __computeImagePoint(self):
        for i in range(len(self.wheelLine_u)):
            if math.isclose(self.wheelLine_u[i], self.u_max, abs_tol=1):
                self.imagePoint = (self.wheelLine_u[i], self.wheelLine_v[i])

    def __computeWheelLine(self):
        wheelLine = np.poly1d(self.coefficients)
        self.wheelLine_u = np.arange(self.u_min, self.u_max + 100, 1)
        self.wheelLine_v = wheelLine(self.wheelLine_u)

    def __computeWheels(self):
        initialRearWheel, initialFrontWheel = self.__locateWheels()
        optimisedRearWheelIndex = self.__optimiseWheelSelection(int(initialRearWheel[2]))
        optimisedFrontWheelIndex = self.__optimiseWheelSelection(int(initialFrontWheel[2]))
        self.rearWheel = (self.u[optimisedRearWheelIndex], self.v[optimisedRearWheelIndex])
        self.frontWheel = (self.u[optimisedFrontWheelIndex], self.v[optimisedFrontWheelIndex])

    def __optimiseWheelSelection(self, wheelIndex):
        wheel_u = self.u[wheelIndex]
        wheel_v = self.v[wheelIndex]

        if self.v[wheelIndex + 1] >= wheel_v:
            if self.u[wheelIndex + 1] > wheel_u:
                wheelIndex = self.__optimiseWheelSelection(wheelIndex + 1)
        if self.v[wheelIndex - 1] >= wheel_v:
            if self.u[wheelIndex - 1] > wheel_u:
                wheelIndex = self.__optimiseWheelSelection(wheelIndex - 1)
        return wheelIndex

    def __locateWheels(self):
        maximaArray = np.array(self.maxima)
        maximaArray = maximaArray[maximaArray[:, 0].argsort()][::-1]
        maximaList = maximaArray.tolist()
        rearWheelList = []
        frontWheel = maximaList.pop(0)
        for maximum in maximaList:
            try:
                if (
                        maximum[1] > frontWheel[1]
                        and maximum[0] < frontWheel[0]
                ):
                    rearWheelList.append(maximum)
            except IndexError:
                print("stop")
        rearWheelArray = np.array(rearWheelList)
        rearWheelArray = rearWheelArray[rearWheelArray[:, 1].argsort()][::-1]
        rearWheel = rearWheelArray.tolist()[0]

        return rearWheel, frontWheel

    def __setMaxima(self):
        for maximum_i in self.maxima_i_filtered:
            self.maxima.append((self.u[maximum_i], self.v[maximum_i], maximum_i))
            if self.verbose:
                print("maximum: {}, {}, i: {}".format(self.u[maximum_i], self.v[maximum_i], maximum_i))

    def __filterMaxima(self):
        threshold = self.v_min + (self.v_max - self.v_min) / 2
        for maximum_i in self.maxima_i[0]:
            if self.v[maximum_i] >= threshold:
                self.maxima_i_filtered.append(maximum_i)


class PointGenerator:
    def __init__(self, annotationsDir):
        self.annotationsDir = annotationsDir
        self.autoPoints = []

        annotationFiles = os.listdir(self.annotationsDir)
        for annotationFile in annotationFiles:
            filePath = os.path.join(annotationsDir, annotationFile)

            self.autoPoints.append(FrontRightPoint(filePath, True))


if __name__ == '__main__':
    pg = PointGenerator(os.path.join(PROJECTS_DIR, "20191125_IM_1_split_053", "annotations", "points"))
    print("The End.")
    fig, ax = plt.subplots(1, 1)
    pg.autoPoints[0].plotAllPoints(axis=ax)
    pg.autoPoints[0].plotWheelLine(axis=ax)
    print(pg.autoPoints[0].imagePoint)

    ax.axis("equal")
    ax.set_xlabel("u")
    ax.set_xlim([0, 800])
    ax.set_ylim([0, 600])
    ax.set_ylabel("v")
    ax.invert_yaxis()
    plt.show()
