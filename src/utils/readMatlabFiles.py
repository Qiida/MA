import os
import re
from scipy.io import loadmat
from mat73 import loadmat as loadmat73


def readMatFile(path):
    matFile = None
    path = checkPathEnding(path)

    if matFile is None:
        matFile = __load73(path)
    if matFile is None:
        matFile = __load(path)
    if matFile is None:
        print("{} is not a MATLAB file.".format(path))
        raise TypeError

    return matFile


def __load(path):
    if os.path.isfile(path):
        try:
            matFile = loadmat(path)
            return __cleanMatFile(matFile)
        except TypeError:
            return None


def __load73(path):
    if os.path.isfile(path):
        try:
            return loadmat73(path)
        except TypeError:
            return None


def checkPathEnding(path):
    if not path.endswith(".mat"):
        path += ".mat"
    return path


def __cleanMatFile(matFile):
    matFile.pop("__header__")
    matFile.pop("__version__")
    matFile.pop("__globals__")
    return matFile


def findMatFiles(path, printResult=False):
    regx = re.compile("(\w+).mat")
    files = [re.search(regx, f).group(1) for f in os.listdir(path)
             if os.path.isfile(os.path.join(path, f))]

    if printResult:
        print("Following mat-Files were found: ")
        for file in files:
            print(file)

    return files


def readMatFiles(dirPath):
    try:
        assert os.path.exists(dirPath)
        matFiles = dict()
        files = findMatFiles(path=dirPath)

        for file in files:
            filePath = os.path.join(dirPath, file)
            matFiles.update({file: readMatFile(filePath + ".mat")})
        return matFiles

    except AssertionError:
        print("{} is not a correct path.".format(dirPath))




