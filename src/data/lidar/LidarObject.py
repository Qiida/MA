from abc import ABC

import matplotlib
import numpy as np
from src.data.lidar.boundingBox.BoundingBox import BoundingBox

matplotlib.use("TkAgg")


class LidarObject(ABC):

    def __init__(self, data, lidarParameter, classification, color):

        # Public.
        self.ID = lidarParameter.ID
        self.data = data
        self.classification = classification
        self.coordinates = lidarParameter.coordinates
        self.objNr = lidarParameter.objNr
        self.idNr = lidarParameter.idNr
        self.timeCan = lidarParameter.timeCan
        self.courseAngle = lidarParameter.courseAngle
        self.boundingBox = self.__buildBoundingBox(color)

    def __buildBoundingBox(self, color):
        length, width = self.__getObjectBoxSize()
        # TODO: implement height method
        height = 1.5
        lineWidth = 1.5
        return BoundingBox(width=width, length=length, height=height, color=color,
                           lineWidth=lineWidth, lidarObject=self)

    def __getObjectBoxSize(self):
        objectBoxSizeX = np.transpose(self.data["ObjBoxSizeX"])[self.objNr][self.idNr]
        index = np.nonzero(np.isfinite(objectBoxSizeX))[0][0]
        objectBoxSizeX = objectBoxSizeX[index]

        objectBoxSizeY = np.transpose(self.data["ObjBoxSizeY"])[self.objNr][self.idNr]
        index = np.nonzero(np.isfinite(objectBoxSizeY))[0][0]
        objectBoxSizeY = objectBoxSizeY[index]
        return objectBoxSizeX, objectBoxSizeY

    def plotBoundingBoxIdNr(self, axis, idNr):

        index = self.getIndex(idNr)
        coordinates = self.coordinates[index]
        courseAngle = self.courseAngle[index]
        self.boundingBox.draw(axis, coordinates, courseAngle)


    def getIndex(self, idNr):
        for index, _idNr in enumerate(np.nditer(self.idNr)):
            if idNr == _idNr:
                return index
