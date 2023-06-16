import re

import numpy as np


def writeCalibration(calibrationMatrix, distortionCoefficients, file):
    f = open(file, "w")
    f.write("[CalibrationMatrix]\n")
    f.write(
        "{},{},{}\n"
        "{},{},{}\n"
        "{},{},{}\n".format(
            calibrationMatrix[0][0], calibrationMatrix[0][1], calibrationMatrix[0][2],
            calibrationMatrix[1][0], calibrationMatrix[1][1], calibrationMatrix[1][2],
            calibrationMatrix[2][0], calibrationMatrix[2][1], calibrationMatrix[2][2]
        )
    )

    f.write("\n")
    f.write("[DistortionCoefficients]\n")
    f.write(
        "{},{},{},{},{}".format(
            distortionCoefficients[0][0],
            distortionCoefficients[0][1],
            distortionCoefficients[0][2],
            distortionCoefficients[0][3],
            distortionCoefficients[0][4]
        )
    )


def loadCalibration(file, verbose=False):
    cameraMatrix = np.zeros(shape=(3, 3), dtype=np.float64)
    distortionCoefficients = np.zeros(shape=(1, 5), dtype=np.float64)

    file = open(file)
    content = file.read()
    rows = content.split("\n")
    rowOfCalibrationMatrix = None
    rowOfDistortionCoefficients = None
    patternCalibrationMatrix = re.compile("\[CalibrationMatrix]")
    patternDistortionCoefficients = re.compile("\[DistortionCoefficients]")

    for i, row in enumerate(rows):
        if i != 0:
            if rowOfCalibrationMatrix is None:
                rowOfCalibrationMatrix = __getMatchedRow(i, patternCalibrationMatrix, rows)
            if rowOfDistortionCoefficients is None:
                rowOfDistortionCoefficients = __getMatchedRow(i, patternDistortionCoefficients, rows)

            if rowOfCalibrationMatrix is not None:
                calibrationMatrixIndex = i - rowOfCalibrationMatrix
                if calibrationMatrixIndex < 3:
                    columns = row.split(",")
                    for j, column in enumerate(columns):
                        if verbose:
                            print(
                                "i: {}\n"
                                "j: {}\n"
                                "CalibrationMatrixIndex: {}\n"
                                "Entry: {}"
                                .format(i, j, calibrationMatrixIndex, column)
                            )
                        cameraMatrix[calibrationMatrixIndex][j] = float(column)
            if rowOfDistortionCoefficients is not None:
                columns = row.split(",")
                for j, column in enumerate(columns):
                    if verbose:
                        print(
                            "i: {}\n"
                            "j: {}\n"
                            "Entry: {}"
                            .format(i, j, column)
                        )

                    distortionCoefficients[0][j] = float(column)
    if verbose:
        print("CAMERA MATRIX:\n{}\n\nDISTORTION COEFFICIENTS:\n{}".format(cameraMatrix, distortionCoefficients))

    return cameraMatrix, distortionCoefficients


def __getMatchedRow(i, pattern, rows):
    if pattern.match(rows[i - 1]):
        return i
