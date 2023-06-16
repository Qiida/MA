from os.path import join

import numpy as np
from matplotlib import pyplot as plt


from src.data.TestVehicle import TestVehicle
from src.data.lidar.LidarParameter import LidarParameter
from src.data.lidar.lidarobjects.Bike import Bike
from src.data.lidar.lidarobjects.Car import Car
from src.data.lidar.lidarobjects.NotClassified import NotClassified
from src.data.lidar.lidarobjects.Pedestrian import Pedestrian
from src.data.lidar.lidarobjects.Truck import Truck
from src.data.lidar.lidarobjects.UnknownBig import UnknownBig
from src.data.lidar.lidarobjects.UnknownClass import UnknownClass
from src.data.lidar.lidarobjects.UnknownSmall import UnknownSmall

from src.data.preparation.computeObjectCenter import computeObjectCenter_x_y
from src.data.preparation.filterNanColumns import filterNanColumns
from src.utils.directories import LIDAR_DIR
from src.utils.readMatlabFiles import readMatFile
import matplotlib
matplotlib.use("TkAgg")

def getLidarObjects(split):
    data = readMatFile(join(LIDAR_DIR, split))["data"]
    filterNanColumns(data)
    return LidarObjectFactory(data["object_laser_raw"]).lidarObjects


def plotLidarObjects(_axis, _lidarObjects, idNr):
    for lidarObject in _lidarObjects.values():
        try:
            if idNr in lidarObject.idNr[0]:
                lidarObject.plotBoundingBoxIdNr(_axis, idNr)
        except:
            print("oh no")

class LidarObjectFactory:

    def __init__(self, objectLaserRaw):

        # Public.
        self.ID = None
        self.data = None
        self.classification = None
        self.lidarObjects = None
        self.timeCan = None
        self.identificationNumber = None
        self.objectCoordinates = None
        self.courseAngle = None

        self.__initialize(objectLaserRaw)
        self.__produce()


    def output(self):
        return self.lidarObjects


    def __getIdentificationNumber(self, objNr):
        return np.where(~np.isnan(self.classification[objNr]))

    def __initialize(self, objectLaserRaw):
        self.data = objectLaserRaw
        self.ID = np.transpose(self.data["objectIDList"])
        self.classification = np.transpose(self.data["Classification"])
        self.lidarObjects = dict()
        self.timeCan = self.data["time_can"]
        self.identificationNumber = np.array(range(self.timeCan.shape[0]))
        self.objectCoordinates = self.__getObjectCoordinates()
        self.courseAngle = np.transpose(self.data["ObjCourseAngle"])


    def __getObjectCoordinates(self):
        objectCenterX, objectCenterY = computeObjectCenter_x_y(self.data)
        return np.transpose(objectCenterX), np.transpose(objectCenterY)


    def __produce(self):
        for objNr, ID in enumerate(self.ID):
            idNr = self.__getIdentificationNumber(objNr)
            timeCan = self.timeCan[idNr]
            self.lidarObjects[ID] = self.__buildLidarObject(ID, objNr, idNr, timeCan)


    def __getClassification(self, idNr, objNr):
        classification = self.classification[objNr][idNr]
        if np.all(classification == classification[0]):
            classification = classification[0]
            return classification
        else:
            print("somethings wrong")


    def __getLidarParameter(self, ID, objNr, idNr, timeCan):
        coordinates = np.vstack((self.objectCoordinates[0][objNr][idNr],
                                 self.objectCoordinates[1][objNr][idNr])).transpose()
        courseAngle = self.courseAngle[objNr][idNr]
        return LidarParameter(ID, objNr, idNr, coordinates, timeCan, courseAngle)


    def __buildLidarObject(self, ID, objNr, idNr, timeCan):
        lidarParameter = self.__getLidarParameter(ID, objNr, idNr, timeCan)
        classification = self.__getClassification(idNr, objNr)
        match classification:
            case 0:
                return NotClassified(self.data, lidarParameter)
            case 1:
                return UnknownSmall(self.data, lidarParameter)
            case 2:
                return UnknownBig(self.data, lidarParameter)
            case 3:
                return Pedestrian(self.data, lidarParameter)
            case 4:
                return Bike(self.data, lidarParameter)
            case 5:
                return Car(self.data, lidarParameter)
            case 6:
                return Truck(self.data, lidarParameter)
            case 17:
                return UnknownClass(self.data, lidarParameter)




if __name__ == '__main__':
    # lObjects = getLidarObjects("Export_pp_20191125_IM_1_split_053")
    # obj28 = lObjects[28]

    figure = plt.figure()
    axis = figure.add_subplot(projection="3d")
    # set_axis(axis=self.axisLidarObjects)
    #
    # axis = plt.axes(projection='3d', axis="equal")
    axis.axis("auto")
    axis.set_xlabel("x")
    axis.set_ylabel("y")
    axis.set_xlim([-15, 15])
    axis.set_ylim([-15, 15])
    axis.set_zlim([-15, 15])
    axis.azim = -180
    axis.elev = 90

    tv = TestVehicle("TEASY3")
    tv.boundingBox.draw(axis)
    data = readMatFile(join(LIDAR_DIR, "Export_pp_20191125_IM_1_split_053"))["data"]
    filterNanColumns(data)
    lidarObjects = LidarObjectFactory(data["object_laser_raw"]).lidarObjects
    plotLidarObjects(axis, lidarObjects, 0)
    plt.show()

    # return LidarObjectFactory(data["object_laser_raw"]).lidarObjects
