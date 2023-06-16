from os.path import join

import matplotlib
import matplotlib.pyplot as plt

from math import isclose

from src.app.plot.setAxis import set_axis
from src.data.TestVehicle import TestVehicle
from src.data.cam.Cam import Cam
from src.data.lidar.LidarObjectFactory import LidarObjectFactory
from src.data.preparation.filterNanColumns import filterNanColumns

from src.lcm.Frame import Frame
from src.lcm.LcmException import LcmMissingDataException, raiseMissingDataException
from src.utils.directories import ROOT_DIR, LIDAR_DIR, CAM_DIR
from src.utils.readMatlabFiles import readMatFile

matplotlib.use("TkAgg")


class LidarCameraMapper:

    def __init__(self, testVehicle=None, matFile=None, camFile=None):

        # Public.
        self.camData = None
        self.camFrames = None
        self.testVehicle = None
        self.lidarEgo = None
        self.lidarData = None
        self.lidarObjects = None
        self.lidarObjectFactory = None
        self.frames = None

        # Private.
        self.__lidarFile = None
        self.__camFile = None
        self.timeCan = None

        self.__initialize(matFile, camFile, testVehicle)

    def getMatFile(self):
        return self.__lidarFile

    def getTimeCan(self):
        return self.timeCan

    def __initialize(self, matFile, camFile, testVehicle):
        self.camFrames = list()
        self.loadTestVehicle(testVehicle)
        self.loadAndPrepareData(matFile=matFile, camFile=camFile)

    def __extractFrames(self):
        frame = self.camData.getNextFrame()
        while frame is not None:
            self.camFrames.append(frame)
            frame = self.camData.getNextFrame()

    def loadTestVehicle(self, testVehicle):
        if testVehicle is None:
            raiseMissingDataException(lcm=self,
                                      message="Test vehicle is missing.")
        self.testVehicle = testVehicle

    def loadAndPrepareData(self, matFile, camFile):
        self.__loadAndPrepareLidarData(matFile)
        self.__loadAndPrepareCamData(camFile)

    def __loadAndPrepareLidarData(self, matFile):
        self.loadLidarFile(matFile)
        self.processLidarData()

    def __loadAndPrepareCamData(self, camFile):
        self.loadCamFile(camFile)
        self.__extractFrames()

    def loadLidarFile(self, matFile=None):
        if matFile is None:
            raiseMissingDataException(lcm=self,
                                      message="Lidar Matlab file is missing.")
        try:
            self.lidarData = readMatFile(path=matFile)["data"]
        except TypeError as error:
            print(error)

    def loadCamFile(self, camFile=None):
        if camFile is None:
            raiseMissingDataException(lcm=self,
                                      message="Cam file is missing.")
        self.camData = Cam(camFile)

    def processLidarData(self):
        if self.lidarData is None:
            raise LcmMissingDataException(lcm=self)

        filterNanColumns(self.lidarData)
        self.lidarObjectFactory = LidarObjectFactory(self.lidarData["object_laser_raw"])
        self.lidarObjects = self.lidarObjectFactory.lidarObjects
        self.__initializeTimeCan()

    def __initializeTimeCan(self):
        self.__extractTimeCan()
        self.__normalizeTimeCan()

    def __normalizeTimeCan(self):
        self.timeCan -= self.timeCan[0]

    def __extractTimeCan(self):
        self.timeCan = self.lidarData["t"]

    def plotLidarObjects(self, idNr, axis):
        for lidarObject in self.lidarObjects.values():
            try:
                if idNr in lidarObject.idNr[0]:
                    lidarObject.plotBoundingBoxIdNr(axis, idNr)
            except AttributeError:
                pass
            except:
                print(lidarObject.ID)

    def produceFramesPNG(self, identificationNumbers=None):
        figure = plt.figure()
        ax = figure.add_subplot(111, projection="3d")

        if identificationNumbers is None:
            identificationNumbers = self.lidarObjectFactory.identificationNumber

        frameNr = 0
        for idNr in identificationNumbers:
            if idNr % 4 == 0:
                set_axis(axis=ax)
                plt.axis('off')
                self.testVehicle.boundingBox.draw(ax)
                for lidarObject in self.lidarObjects:
                    try:
                        if idNr in lidarObject.idNr[0]:
                            lidarObject.plotBoundingBoxIdNr(ax, idNr)
                    except AttributeError:
                        pass

                plt.savefig(join(ROOT_DIR, "output", "images", "frame_{}.png".format(frameNr)), dpi=500)
                plt.cla()
                print("Exported frame_{}".format(frameNr))
                frameNr += 1

    def map(self, time):
        for idNr, timeStep in enumerate(self.timeCan):
            if isclose(time, timeStep, abs_tol=1e-2):
                return idNr

    def buildFrames(self):
        if self.frames is None:
            self.frames = list()

        for frameNr, frame in enumerate(self.camFrames):
            self.frames.append(self.buildFrame(frameNr, frame))

        return self.frames

    def buildFrame(self, frameNr, frame):
        time = frameNr / self.camData.getFPS()
        return Frame(ID=frameNr,
                     image=frame,
                     time=time,
                     idNr=self.map(time))


if __name__ == '__main__':
    lcMapper = LidarCameraMapper(testVehicle=TestVehicle("TEASY3"),
                                 matFile=join(LIDAR_DIR, "Export_pp_20191125_IM_1_split_053.mat"),
                                 camFile=join(CAM_DIR, "20191125_IM_1_split_053_back.avi"))

    # images = lcMapper.buildFrames()
    lcMapper.produceFramesPNG()

    print("stop")
#
