import math
import os
import json
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from scipy import linalg

from scipy.signal import find_peaks

from src.utils.directories import PROJECTS_DIR

matplotlib.use("TkAgg")

SPLIT = "20191125_IM_1_split_053"
ANNOTATIONS_DIR = os.path.join(PROJECTS_DIR, SPLIT, "annotations", "points")


def __createLeftMatrix(*dims):
    _data = [dim.flatten() for dim in dims]
    _data.append(np.ones_like(_data[0]))
    return np.asarray(_data).transpose()


def __computeBestFitParameters(left_matrix, right_vector):
    v_vector = right_vector.flatten()
    left_matrix_pseudo_inverse = linalg.pinv(left_matrix)
    return left_matrix_pseudo_inverse @ v_vector


def computeFittingV(*dims, right_vector):
    _left_matrix = __createLeftMatrix(*dims)
    _params = __computeBestFitParameters(_left_matrix, right_vector)
    _v_fit = _left_matrix @ _params
    return _v_fit.reshape(right_vector.shape)


def findLocalMaxima(array):
    return find_peaks(array)


def __findLocalMaximaMinima(N, array):
    # Empty lists to store points of
    # local maxima and minima
    _maxima = []
    _minima = []

    # Checking whether the first point is
    # local maxima or minima or neither
    if array[0] > array[1]:
        _maxima.append(0)
    elif array[0] < array[1]:
        _minima.append(0)

    # Iterating over all points to check
    # local maxima and local minima
    for i in range(1, N - 1):

        # Condition for local minima
        if array[i - 1] > array[i] < array[i + 1]:
            _minima.append(i)

        # Condition for local maxima
        elif array[i - 1] < array[i] > array[i + 1]:
            _maxima.append(i)

    # Checking whether the last point is
    # local maxima or minima or neither
    if array[-1] > array[-2]:
        _maxima.append(N - 1)
    elif array[-1] < array[-2]:
        _minima.append(N - 1)

        # Print all the local maxima and
        # local minima indexes stored
    if len(_maxima) > 0:
        print("Points of Local maxima are : ", end='')
        print(*_maxima)
    else:
        print("There are no points of Local maxima.")

    if len(_minima) > 0:
        print("Points of Local minima are : ", end='')
        print(*_minima)
    else:
        print("There are no points of Local minima.")

    return _maxima, _minima


def containsGlobalMaximum(localMaxima, globalMaximum):
    for _i in range(len(localMaxima)):
        if localMaxima[_i] == globalMaximum:
            return True
    return False


def set_u_max():
    global u_max, u_max_i
    u_max = u[i]
    u_max_i = i


def set_u_min():
    global u_min, u_min_i
    u_min = u[i]
    u_min_i = i


def set_v_max():
    global v_max, v_max_i
    v_max = v[i]
    v_max_i = i


def set_v_min():
    global v_min, v_min_i
    v_min = v[i]
    v_min_i = i


def printGlobalMaxima():
    print("u_max: {}, i: {}".format(u_max, u_max_i))
    print("u_min: {}, i: {}".format(u_min, u_min_i))
    print("v_max: {}, i: {}".format(v_max, v_max_i))
    print("v_min: {}, i: {}".format(v_min, v_min_i))


def locateWheels(_maxima):
    maximaArray = np.array(_maxima)
    maximaArray = maximaArray[maximaArray[:, 0].argsort()][::-1]
    maximaList = maximaArray.tolist()
    rearWheelList = []
    _frontWheel = maximaList.pop(0)
    for maximum in maximaList:
        if (
                maximum[1] > _frontWheel[1]
                and maximum[0] < _frontWheel[0]
        ):
            rearWheelList.append(maximum)
    rearWheelArray = np.array(rearWheelList)
    rearWheelArray = rearWheelArray[rearWheelArray[:, 1].argsort()][::-1]
    _rearWheel = rearWheelArray.tolist()[0]
    return _frontWheel, _rearWheel


def optimiseWheelSelection(wheelIndex, _u, _v):
    wheel_u = _u[wheelIndex]
    wheel_v = _v[wheelIndex]

    if _v[wheelIndex + 1] >= wheel_v:
        if _u[wheelIndex + 1] > wheel_u:
            wheelIndex = optimiseWheelSelection(wheelIndex + 1, _u, _v)
    if _v[wheelIndex - 1] >= wheel_v:
        if _u[wheelIndex - 1] > wheel_u:
            wheelIndex = optimiseWheelSelection(wheelIndex - 1, _u, _v)
    return wheelIndex


def extractPoints(_filePath):
    f = open(_filePath)
    _u = []
    _v = []
    data = json.load(f)
    points = data["annotations"][0]["polygon"]["paths"][0]
    for point in points:
        _u.append(point["x"])
        _v.append(point["y"])
    return _u, _v


if __name__ == '__main__':

    annotationFiles = os.listdir(ANNOTATIONS_DIR)
    for annotationFile in annotationFiles:
        filePath = os.path.join(ANNOTATIONS_DIR, annotationFile)

        u, v = extractPoints(filePath)

        u_max, u_min, v_max, v_max_i = -1, -1, -1, -1
        u_max_i, u_min_i, v_min, v_min_i = -1, -1, -1, -1

        for i in range(len(u)):

            if u_max == -1:
                set_u_max()
                set_u_min()

            if u_max < u[i]:
                set_u_max()

            if u_min > u[i]:
                set_u_min()

            if v_max == -1:
                set_v_max()
                set_v_min()

            if v_max < v[i]:
                set_v_max()

            if v_min > v[i]:
                set_v_min()

        printGlobalMaxima()

        # maxima_i, minima_i = findLocalMaximaMinima(N=len(u), array=v)

        v_fit = computeFittingV(np.array(u), right_vector=np.array(v))
        v_leveled = np.subtract(v, v_fit)

        maxima_i = findLocalMaxima(v_leveled)
        # if not containsGlobalMaximum(localMaxima=maxima_i, globalMaximum=v_max_i):
        #     maxima_i.append(v_max_i)

        # if not containsGlobalMaximum(localMaxima=minima_i, globalMaximum=v_min_i):
        #     minima_i.append(v_min_i)

        threshold = v_min + (v_max - v_min) / 2

        maxima_i_filtered = []
        for maximum_i in maxima_i[0]:
            if v[maximum_i] >= threshold:
                maxima_i_filtered.append(maximum_i)

        maxima, minima = [], []

        for maximum_i in maxima_i_filtered:
            maxima.append((u[maximum_i], v[maximum_i], maximum_i))
            print("maximum: {}, {}, i: {}".format(u[maximum_i], v[maximum_i], maximum_i))

        # for minimum_i in minima_i:
        #     minima.append((u[minimum_i], v[minimum_i]))
        #     print("minimum: {}, {}, i: {}".format(u[minimum_i], v[minimum_i], minimum_i))

        initialFrontWheel, initialRearWheel = locateWheels(maxima)

        optimisedRearWheelIndex = optimiseWheelSelection(int(initialRearWheel[2]), u, v)
        optimisedFrontWheelIndex = optimiseWheelSelection(int(initialFrontWheel[2]), u, v)

        rearWheel = (u[optimisedRearWheelIndex], v[optimisedRearWheelIndex])
        frontWheel = (u[optimisedFrontWheelIndex], v[optimisedFrontWheelIndex])

        wheels_u = [rearWheel[0], frontWheel[0]]
        wheels_v = [rearWheel[1], frontWheel[1]]
        coefficients = np.polyfit(wheels_u, wheels_v, 1)

        print("a =", coefficients[0])
        print("b =", coefficients[1])

        wheelLine = np.poly1d(coefficients)
        wheelLine_u = np.arange(u_min, u_max + 100, 1)
        wheelLine_v = wheelLine(wheelLine_u)

        imagePoint = None
        for i in range(len(wheelLine_u)):
            if math.isclose(wheelLine_u[i], u_max, abs_tol=1):
                imagePoint = (wheelLine_u[i], wheelLine_v[i])

        print(imagePoint)

        plt.title(annotationFile)

        plt.plot(wheelLine_u, wheelLine_v)

        plt.plot([u_max, u_max], [0, 600], 0.2, c="c")
        # plt.plot([u_min, u_min], [0, 600], 0.2, c="c")
        # plt.plot([0, 800], [v_max, v_max], 0.2, c="c")
        # plt.plot([0, 800], [v_min, v_min], 0.2, c="c")

        plt.scatter(
            x=u,
            y=v,
            s=2,
            c="k"
        )

        plt.scatter(
            x=u,
            y=v_leveled,
            s=2,
            c="c"
        )

        # plt.scatter(
        #     x=np.array(maxima)[:, 0],
        #     y=np.array(maxima)[:, 1],
        #     s=4,
        #     c="r"
        # )


        plt.scatter(frontWheel[0], frontWheel[1], 15, color="r")
        plt.scatter(rearWheel[0], rearWheel[1], 15, color="r")


        axis = plt.gca()
        axis.axis("equal")
        axis.set_xlabel("u")
        axis.set_xlim([0, 800])
        axis.set_ylim([0, 600])
        axis.set_ylabel("v")
        axis.invert_yaxis()
        plt.show()
