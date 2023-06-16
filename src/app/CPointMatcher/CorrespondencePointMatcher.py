import json
import os
import sys
from math import isclose

import cv2
import re

import numpy as np
from PyQt5.QtWidgets import QApplication, QVBoxLayout
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg

from src.app.CPointMatcher.Annotation import Annotation, AnnotationStyle
from src.app.CPointMatcher.Frame import Frame
from src.app.CPointMatcher.MainWindow import MainWindow
from src.app.CPointMatcher.PointGenerator import FrontRightPoint
from src.app.plot.setAxis import set_axis
from src.data.TestVehicle import TestVehicle
from src.data.lidar.LidarObjectFactory import LidarObjectFactory
from src.data.preparation.filterNanColumns import filterNanColumns

from src.utils.directories import LIDAR_DIR, PROJECTS_DIR
from src.utils.readMatlabFiles import readMatFile


def extractPointPairs(correspondencePointsFile, lidarObjects):
    f = open(correspondencePointsFile)
    content = f.read()
    rows = content.split("\n")
    rows.pop(0)

    frames = []
    imagePoints = []
    objectPoints = []

    for column in rows:
        print(column)
        splits = column.split(" ")
        try:
            imagePoints.append((float(splits[1]), float(splits[2])))
            frames.append(int(splits[0]))
        except ValueError:
            print("stop")

        idNr = int(splits[3])
        ID = int(splits[4])
        vertex = int(splits[5])
        try:
            objectPoints.append(lidarObjects[ID].boundingBox.getCornersFromIdNr(idNr)[vertex])
        except IndexError:
            print("*** Error ***: {}".format(column))

    return frames, imagePoints, objectPoints


class CorrespondenceMatcher:

    def __init__(self, split, resourcesDir, testVehicle, annotationStyle, useUndistorted=False):

        self.__split = split
        self.__testVehicle = testVehicle
        self.__useUndistorted = useUndistorted

        self.annotations = []
        self.annotationStyle = annotationStyle

        self.resourcesDir = resourcesDir
        self.annotationsDirectory = None
        self.imagesDirectory = None

        self.files = []
        self.frames = []

        # GUI
        self.app = None
        self.mainWindow = None
        self.frameIndex = 0
        self.pointIndex = 0
        self.annotationIndex = 0

        self.outputFile = open(os.path.join(self.resourcesDir, "out", "autopoints.txt"), "a")
        self.seperator = " "

        self.lidarObjects = None
        self.axisLidarObjects = None
        self.axisImage = None

        self.figure = None
        self.timeCan = None

        self.autoPoints = dict()

        self.__initialize()


    def __initialize(self):

        if self.annotationStyle == AnnotationStyle.LAYOUT:
            self.annotationsDirectory = os.path.join(self.resourcesDir, "annotations", "layout")
        elif self.annotationStyle == AnnotationStyle.POINTS:
            self.annotationsDirectory = os.path.join(self.resourcesDir, "annotations", "points")

        if self.__useUndistorted:
            self.imagesDirectory = os.path.join(self.resourcesDir, "images", "undistorted")
        else:
            self.imagesDirectory = os.path.join(self.resourcesDir, "images", "gray")

        files = os.listdir(self.annotationsDirectory)
        for file in files:
            self.files.append(file.split(".")[0])

        self.__initializeLidarObjects()
        self.__buildFrames()
        self.__initializeFigure()
        self.__initializeGUI()

    def __initializeGUI(self):
        self.app = QApplication(sys.argv)
        self.mainWindow = MainWindow(self)
        self.canvas = FigureCanvasQTAgg(figure=self.figure)
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.mainWindow.frameCanvas.setLayout(layout)
        self.draw()
        self.mainWindow.show()
        self.app.exec()
        self.outputFile.close()

    def __initializeLidarObjects(self):
        matFile = self.__findMatFile()
        data = readMatFile(os.path.join(LIDAR_DIR, matFile))["data"]
        self.timeCan = data["t"]
        self.timeCan -= self.timeCan[0]
        filterNanColumns(data)
        self.lidarObjects = LidarObjectFactory(data["object_laser_raw"]).lidarObjects

    def __findMatFile(self):
        files = os.listdir(LIDAR_DIR)
        for file in files:
            regx = re.compile(self.__split)
            search = re.search(regx, file)
            if search is not None:
                return file
        return None

    def __buildFrames(self):
        for file in self.files:
            image = cv2.imread(os.path.join(self.imagesDirectory, file + ".png"))
            frameNr = int(file)

            points = []
            annotations = []

            if self.annotationStyle == AnnotationStyle.LAYOUT:

                f = open(os.path.join(self.annotationsDirectory, file + ".json"), "r")
                jsonFile = json.load(f)

                for a in jsonFile["annotations"]:
                    dataPoints = a["polygon"]["paths"][0]
                    for point in dataPoints:
                        points.append(np.array((point["x"], point["y"])))
                    annotations.append(Annotation(frameNr, np.array(points)))
                    points.clear()

                time = 1 / 25 * frameNr
                self.frames.append(Frame(frameNr, annotations, image, self.map(time)))

            if self.annotationStyle == AnnotationStyle.POINTS:

                try:
                    autoPoint = FrontRightPoint(os.path.join(self.annotationsDirectory, file + ".json"))
                    annotations.append(Annotation(frameNr, np.array(autoPoint.imagePoint)))
                    self.autoPoints[frameNr] = autoPoint
                    time = 1 / 25 * frameNr
                    self.frames.append(Frame(frameNr, annotations, image, self.map(time)))
                except IndexError:
                    print("Error: {}".format(file))



    def map(self, time):
        for idNr, timeStep in enumerate(self.timeCan):
            if isclose(time, timeStep, abs_tol=1e-2):
                return idNr

    def __initializeFigure(self):
        self.figure = plt.figure()
        self.axisLidarObjects = self.figure.add_subplot(211, projection="3d")
        set_axis(axis=self.axisLidarObjects)
        self.axisImage = self.figure.add_subplot(212)

    def draw(self):
        self.axisImage.imshow(self.frames[self.frameIndex].image)
        self.__plotLidarObjects(self.frames[self.frameIndex].idNr)
        self.__plotAnnotations()
        self.__plotPointOfInterest()

        self.figure.suptitle('Frame: {}\nidNr: {}'.format(self.frames[self.frameIndex].frameNr, self.frames[self.frameIndex].idNr))

    def __plotLidarObjects(self, idNr):
        self.__testVehicle.boundingBox.draw(self.axisLidarObjects)
        for lidarObject in self.lidarObjects.values():
            try:
                if idNr in lidarObject.idNr[0]:
                    lidarObject.plotBoundingBoxIdNr(self.axisLidarObjects, idNr)
            except AttributeError:
                pass
            except IndexError as e:
                print(e)
                print("Error: ObjectID: {} idNr: {}".format(lidarObject.ID, idNr))

    def __plotAnnotations(self):

        if self.annotationStyle == AnnotationStyle.LAYOUT:

            frame = self.frames[self.frameIndex]
            annotation = frame.annotations[self.annotationIndex]
            for point in annotation.points:
                self.axisImage.scatter(point[0], point[1], s=3, c="r")

        if self.annotationStyle == AnnotationStyle.POINTS:
            frame = self.frames[self.frameIndex]
            annotation = frame.annotations[self.annotationIndex]
            self.axisImage.scatter(annotation.points[0], annotation.points[1], s=3, c="r")
            autoPoint = self.autoPoints[frame.frameNr]
            autoPoint.plotAllPoints(self.axisImage)
            autoPoint.plotWheelLine(self.axisImage)
            self.axisImage.plot([autoPoint.u_max, autoPoint.u_max], [autoPoint.v_min, autoPoint.v_max], linewidth=0.2, c="c")

    def __plotPointOfInterest(self):
        point = self.getPointOfInterest()
        self.axisImage.scatter(point[0], point[1], s=10, c="g")

    def getPointOfInterest(self):
        annotation = self.frames[self.frameIndex].annotations[self.annotationIndex]
        if self.annotationStyle == AnnotationStyle.LAYOUT:
            point = annotation.points[self.pointIndex]
            return point
        if self.annotationStyle == AnnotationStyle.POINTS:
            point = annotation.points
            return point

    def resetAxes(self):
        self.axisLidarObjects.clear()
        self.axisImage.clear()
        set_axis(axis=self.axisLidarObjects)

    @staticmethod
    def extractPointPairs(correspondencePointsFile, lidarObjects):
        f = open(correspondencePointsFile)
        content = f.read()
        rows = content.split("\n")
        rows.pop(0)

        frames = []
        imagePoints = []
        objectPoints = []

        for column in rows:
            print(column)
            splits = column.split(" ")
            try:
                imagePoints.append((float(splits[1]), float(splits[2])))
                frames.append(int(splits[0]))
            except ValueError:
                print("stop")

            idNr = int(splits[3])
            ID = int(splits[4])
            vertex = int(splits[5])
            try:
                objectPoints.append(lidarObjects[ID].boundingBox.getCornersFromIdNr(idNr)[vertex])
            except IndexError:
                print("*** Error ***: {}".format(column))

        return frames, imagePoints, objectPoints


if __name__ == '__main__':
    cmatcher = CorrespondenceMatcher(
        split="IM_1_split_053",
        resourcesDir=os.path.join(PROJECTS_DIR, "20191125_IM_1_split_053"),
        testVehicle=TestVehicle("TEASY3"),
        # annotationStyle=AnnotationStyle.LAYOUT,
        annotationStyle=AnnotationStyle.POINTS,
        useUndistorted=True
    )

    print("wow")
