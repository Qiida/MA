import os

import pandas as pd
import torch
import numpy as np
import cv2
from time import time

from src.utils.analysis import buildShortName
from src.data.tracklet.boxes import YoloBox
from src.data.tracklet.yolo.YoloObject import YoloObject


def buildDetectedObjectsFromCSV(path):
    detectedObjects = []
    df = pd.read_csv(path)
    for index, row in df.iterrows():
        detectedObjects.append(
            YoloObject(
                ID=row.ID,
                objectType=row.objectType,
                box=YoloBox(
                    u=(row.u0, row.u1),
                    v=(row.v0, row.v1),
                    imageIndex=row.imageIndex
                )
            )
        )

    return detectedObjects


class ObjectDetector:

    def __init__(self, path, verbose=False, classesOfInterest=None):
        self.verbose = verbose

        # public.
        self.path = path
        self.name = os.path.basename(self.path)
        self.out = None
        self.model = None
        self.classes = None
        self.frames = None
        self.device = None
        self.results = None
        self.detectedObjects = None

        # private.
        self.__ID = None
        self.__u0 = None
        self.__u1 = None
        self.__v0 = None
        self.__v1 = None
        self.__area = None
        self.__objectType = None
        self.__imageIndex = None

        self.__initialize(classesOfInterest)
        self.__compute()
        self.__buildDetectedObjects()
        self.__buildLists()
        self.__drawBoxesOnFrames()

    def __initialize(self, classesOfInterest):

        if classesOfInterest is None:
            self.classesOfInterest = [
                "car",
                "bicycle",
                "truck",
                "bench",
                "backpack",
                "bus",
                "person",
                "plotted plant",
                "skateboard",
                "stop sign"
                "traffic light",
                "umbrella",
                "vase"
            ]
        else:
            self.classesOfInterest = classesOfInterest

        self.out = os.path.join(self.path, "out")
        self.__setDevice()
        self.__loadModel()
        self.__loadFrames()


    def __setDevice(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        if self.verbose:
            print("\n\nDevice Used: ", self.device)


    def __loadModel(self):
        self.model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
        self.classes = self.model.names


    def __loadFrames(self):
        self.frames = []
        imagesDir = os.path.join(self.path, "images")
        for file in os.listdir(imagesDir):
            self.frames.append(
                cv2.imread(os.path.join(imagesDir, file))
            )


    def __compute(self):
        self.results = list()
        for frame in self.frames:
            startTime = time()
            self.results.append(self.scoreFrame(frame))
            endTime = time()
            fps = 1 / np.round(endTime - startTime, 3)
            if self.verbose:
                print(f"FPS: {fps}")


    def exportVideo(self):
        dimensions = self.frames[0].shape
        height = dimensions[0]
        width = dimensions[1]
        fourcc = cv2.VideoWriter_fourcc(*"MJPG")
        out = cv2.VideoWriter(os.path.join(self.out, f"{self.name}.avi"), fourcc, 25, (width, height))

        for frame in self.frames:
            out.write(frame)

        if self.verbose:
            print(f"Video created at {self.out}")

    def exportPNG(self):
        for i in range(len(self.frames)):
            cv2.imwrite(
                os.path.join(self.out, f"{i:010d}.png"),
                self.frames[i]
            )

    def __drawBoxesOnFrames(self):
        for i, frame in enumerate(self.frames):
            results = self.results[i]
            self.frames[i] = self.plotBoxes(results, frame)

    def scoreFrame(self, frame):
        self.model.to(self.device)
        frame = [frame]
        results = self.model(frame)

        labels, cord = results.xyxyn[0][:, -1], results.xyxyn[0][:, :-1]
        return labels, cord

    def classToLabel(self, index):
        return self.classes[int(index)]

    def __buildDetectedObjects(self):
        self.detectedObjects = list()

        for i in range(len(self.frames)):
            self.__buildDetectedObjectsInFrameIndex(i)

    def __buildDetectedObjectsInFrameIndex(self, index):
        labels, coordinates = self.results[index]
        xShape, yShape = self.frames[index].shape[1], self.frames[index].shape[0]

        for i, label in enumerate(labels):
            coordinate = coordinates[i]
            if coordinate[4] >= 0.2:
                label = self.classToLabel(labels[i])
                if self.__isOfInterest(label):

                    u0, v0 = int(coordinate[0] * xShape), int(coordinate[1] * yShape)
                    u1, v1 = int(coordinate[2] * xShape), int(coordinate[3] * yShape)

                    box = YoloBox(
                        u=(u0, u1),
                        v=(v0, v1),
                        imageIndex=index
                    )

                    self.detectedObjects.append(
                        YoloObject(
                            ID=f"{buildShortName(self.name)}_{i}",
                            objectType=label,
                            box=box)
                    )

    def __isOfInterest(self, objectType):
        for classOfInterest in self.classesOfInterest:
            if classOfInterest == objectType:
                return True
        return False

    def plotBoxes(self, results, frame):
        labels, cord = results
        n = len(labels)
        xShape, yShape = frame.shape[1], frame.shape[0]

        for i in range(n):
            row = cord[i]
            if row[4] >= 0.2:
                label = self.classToLabel(labels[i])

                # if self.__isOfInterest(label):
                u0, v0 = int(row[0] * xShape), int(row[1] * yShape)
                u1, v1 = int(row[2] * xShape), int(row[3] * yShape)

                bgr = (0, 255, 0)
                cv2.rectangle(frame, (u0, v0), (u1, v1), bgr, 2)
                cv2.putText(
                    img=frame,
                    text=label,
                    org=(u0, v0),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=0.9,
                    color=bgr
                )
        return frame

    def __buildLists(self):
        self.__ID = list()
        self.__u0 = list()
        self.__u1 = list()
        self.__v0 = list()
        self.__v1 = list()
        self.__area = list()
        self.__objectType = list()
        self.__imageIndex = list()

        for detectedObject in self.detectedObjects:
            self.__ID.append(detectedObject.ID)
            self.__u0.append(detectedObject.box.u[0])
            self.__u1.append(detectedObject.box.u[1])
            self.__v0.append(detectedObject.box.v[0])
            self.__v1.append(detectedObject.box.v[1])
            self.__area.append(detectedObject.box.area)
            self.__objectType.append(detectedObject.objectType)
            self.__imageIndex.append(detectedObject.box.imageIndex)

    def buildDictionary(self):
        dictionary = {
            "ID": self.__ID,
            "objectType": self.__objectType,
            "imageIndex": self.__imageIndex,
            "u0": self.__u0,
            "u1": self.__u1,
            "v0": self.__v0,
            "v1": self.__v1,
            "area": self.__area,
        }
        return dictionary
