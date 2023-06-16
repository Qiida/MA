import os.path

import pandas as pd

from src.data.tracklet.kitti.TrackletFactory import TrackletFactory
from src.data.tracklet.tracklets import YoloTracklet, CombiTracklet
from src.data.tracklet.yolo.ObjectDetector import buildDetectedObjectsFromCSV
from src.utils.directories import ANALYSIS_DIR


class Overlap:
    def __init__(self, diff_u=None, diff_v=None, overlap=None):
        self.diff_u = diff_u
        self.diff_v = diff_v
        self.overlap = overlap

    @staticmethod
    def calculateOverlap(box1, box2):
        x1_min, x1_max, y1_min, y1_max = box1
        x2_min, x2_max, y2_min, y2_max = box2

        widthOverlap = max(0, min(x1_max, x2_max) - max(x1_min, x2_min))
        heightOverlap = max(0, min(y1_max, y2_max) - max(y1_min, y2_min))

        overlapArea = widthOverlap * heightOverlap

        box1_area = (x1_max - x1_min) * (y1_max - y1_min)
        box2_area = (x2_max - x2_min) * (y2_max - y2_min)

        total_area = box1_area + box2_area - overlapArea
        overlap = overlapArea / total_area

        return overlap


class CombiTrackletFactory:
    def __init__(
            self, date, split, yoloObjects, kittiTracklets,
            verbose=False, pixelPrecision=10, overlapThreshold=0.7
    ):

        # public.
        self.pixelPrecision = None
        self.overlapThreshold = None
        self.split = None
        self.trackletKeys = None
        self.kittiTrackletsDict = None
        self.yoloTrackletsDict = None
        self.yoloObjectsByFrame = None
        self.combiTracklets = None

        # private.
        self.__numberOfFrames = None
        self.__yoloObjects = None
        self.__kittiTracklets = None
        self.__foundTracklets = None
        self.__notFoundTracklets = None

        self.__ID = None
        self.__objectType = None
        self.__height = None
        self.__width = None
        self.__length = None
        self.__firstFrame = None
        self.__k_u0 = None
        self.__k_u1 = None
        self.__k_v0 = None
        self.__k_v1 = None
        self.__y_u0 = None
        self.__y_u1 = None
        self.__y_v0 = None
        self.__y_v1 = None

        self.__initialize(date, kittiTracklets, pixelPrecision, split, verbose, yoloObjects, overlapThreshold)

    def __initialize(self, date, kittiTracklets, precision, split, verbose, allYoloObjects, overlapThreshold):
        self.verbose = verbose
        self.pixelPrecision = precision
        self.overlapThreshold = overlapThreshold
        self.split = split

        self.matchedBoxes = []

        self.__foundTracklets = []
        self.__notFoundTracklets = []

        self.__yoloObjects = []
        self.__yoloClassesOfInterest = [
            "car",
            # "cyclist",
            "person",
            "truck",
            "bench",
            "backpack",
            "bus",
            "plotted plant",
            "skateboard",
            "stop sign"
            "traffic light",
            "umbrella",
            "vase"
        ]

        for yoloObject in allYoloObjects:
            if self.__isClassOfInterest(yoloObject.objectType):
                self.__yoloObjects.append(yoloObject)

        self.__kittiTracklets = kittiTracklets

        self.__buildKittiTrackletsDict()
        self.__countFrames(date, split)
        self.__sortYoloObjectsByFrame()
        self.__buildYoloTracklets()
        self.__buildCombiTracklets()

    def __buildCombiTracklets(self):
        self.combiTracklets = list()

        for key in self.__foundTracklets:
            ID = key
            kTracklet = self.kittiTrackletsDict.get(key)
            kBoxes = kTracklet.boxes
            yTracklet = self.yoloTrackletsDict.get(key)
            yBoxes = yTracklet.boxes
            objectType = kTracklet.objectType
            height = kTracklet.height
            width = kTracklet.width
            length = kTracklet.length
            firstFrame = kTracklet.firstFrame
            poses = kTracklet.poses

            self.combiTracklets.append(
                CombiTracklet(
                    ID=ID,
                    objectType=objectType,
                    height=height,
                    width=width,
                    length=length,
                    firstFrame=firstFrame,
                    poses=poses,
                    kTracklet=kTracklet,
                    kBoxes=kBoxes,
                    yTracklet=yTracklet,
                    yBoxes=yBoxes,
                )
            )

    def __buildYoloTracklets(self):
        self.trackletKeys = list()
        self.yoloTrackletsDict = dict()

        for kittiTracklet in self.__kittiTracklets:
            self.trackletKeys.append(kittiTracklet.ID)

            numberOfBoxes = len(kittiTracklet.boxes)
            yBoxes = [None] * numberOfBoxes
            yObjects = [None] * numberOfBoxes

            for i, box in enumerate(kittiTracklet.boxes):
                frame = box.imageIndex
                boxMatched = False

                for yoloObject in self.yoloObjectsByFrame[frame]:
                    if self.verbose:
                        print(f"\n\n[{yoloObject.ID}]")

                    if not boxMatched:
                        diff_u, diff_v = self.__computeDiffs(box, yoloObject.box)
                        overlap = self.__computeOverlap(box, yoloObject)

                        if overlap > self.overlapThreshold or self.__checkPixelPrecision(diff_u, diff_v):
                            yoloObject.box.overlap = Overlap(
                                diff_u, diff_v, overlap
                            )

                            yBoxes[i] = yoloObject.box
                            yObjects[i] = yoloObject
                            boxMatched = True

            # if len(yBoxes) > 0:
            self.yoloTrackletsDict.update(
                {
                    kittiTracklet.ID: YoloTracklet(
                        ID=kittiTracklet.ID,
                        objectType=kittiTracklet.objectType,
                        yoloObjects=yObjects,
                        boxes=yBoxes,
                    )
                }
            )
            self.__foundTracklets.append(kittiTracklet.ID)
            # else:
            #     self.__notFoundTracklets.append(kittiTracklet.ID)


    def __computeOverlap(self, box, yoloObject):
        overlap = Overlap.calculateOverlap(
            box1=(
                box.u[0], box.u[1],
                box.v[0], box.v[1]
            ),
            box2=(
                yoloObject.box.u[0], yoloObject.box.u[1],
                yoloObject.box.v[0], yoloObject.box.v[1]
            )
        )
        if self.verbose:
            print("Overlap computed")
        return overlap

    def __checkPixelPrecision(self, diff_u, diff_v):
        if diff_u[0] > self.pixelPrecision:
            return False
        if diff_u[1] > self.pixelPrecision:
            return False
        if diff_v[0] > self.pixelPrecision:
            return False
        if diff_v[1] > self.pixelPrecision:
            return False
        return True

    def __buildKittiTrackletsDict(self):
        self.kittiTrackletsDict = dict()
        for _tracklet in self.__kittiTracklets:
            self.kittiTrackletsDict.update({_tracklet.ID: _tracklet})

    def __sortYoloObjectsByFrame(self):
        self.yoloObjectsByFrame = list()

        for frame in range(self.__numberOfFrames):
            objects = list()
            for yoloObject in self.__yoloObjects:
                if yoloObject.box.imageIndex == frame:
                    objects.append(
                        yoloObject
                    )
            self.yoloObjectsByFrame.append(objects)

    def __countFrames(self, date, split):
        self.__numberOfFrames = 0
        for _ in os.listdir(os.path.join(ANALYSIS_DIR, date, split, "images")):
            self.__numberOfFrames += 1

    def __isClassOfInterest(self, _type):
        for classOfInterest in self.__yoloClassesOfInterest:
            if classOfInterest == _type:
                return True
        return False

    def __computeDiffs(self, kittiBox, yoloBox):
        diff_u0 = abs(kittiBox.u[0] - yoloBox.u[0])
        diff_u1 = abs(kittiBox.u[1] - yoloBox.u[1])

        diff_v0 = abs(kittiBox.v[0] - yoloBox.v[0])
        diff_v1 = abs(kittiBox.v[1] - yoloBox.v[1])

        if self.verbose:
            print(f"diff_u0: {diff_u0}")
            print(f"diff_u1: {diff_u1}")
            print(f"diff_v0: {diff_v0}")
            print(f"diff_v1: {diff_v1}")

        return (diff_u0, diff_u1), (diff_v0, diff_v1)

    def __buildLists(self):
        self.__ID = list()
        self.__objectType = list()
        self.__imageIndex = list()
        self.__height = list()
        self.__width = list()
        self.__length = list()
        self.__distance = list()

        self.__k_u0 = []
        self.__k_u1 = []
        self.__k_v0 = []
        self.__k_v1 = []
        self.__k_area = []
        self.__y_u0 = []
        self.__y_u1 = []
        self.__y_v0 = []
        self.__y_v1 = []
        self.__y_area = []

        self.__overlap = []
        self.__diff_u0 = []
        self.__diff_u1 = []
        self.__diff_v0 = []
        self.__diff_v1 = []

        for combiTracklet in self.combiTracklets:
            for box in combiTracklet.boxes:
                self.__ID.append(combiTracklet.ID)
                self.__objectType.append(combiTracklet.objectType)
                self.__imageIndex.append(box.imageIndex)
                self.__height.append(combiTracklet.height)
                self.__width.append(combiTracklet.width)
                self.__length.append(combiTracklet.length)
                self.__distance.append(box.distance)
                self.__buildList__k(box)
                self.__buildList__y(box)
                self.__buildList__overlap(box)

    def __buildList__k(self, box):
        self.__k_area.append(box.k_area)
        self.__k_u0.append(box.k_u[0])
        self.__k_u1.append(box.k_u[1])
        self.__k_v0.append(box.k_v[0])
        self.__k_v1.append(box.k_v[1])

    def __buildList__overlap(self, box):
        self.__overlap.append(box.overlap)
        self.__diff_u0.append(box.diff_u[0])
        self.__diff_u1.append(box.diff_u[1])
        self.__diff_v0.append(box.diff_v[0])
        self.__diff_v1.append(box.diff_v[1])

    def __buildList__y(self, box):
        self.__y_area.append(box.y_area)
        self.__y_u0.append(box.y_u[0])
        self.__y_u1.append(box.y_u[1])
        self.__y_v0.append(box.y_v[0])
        self.__y_v1.append(box.y_v[1])

    def __buildDictionary(self):
        self.__dictionary = {
            "ID": self.__ID,
            "objectType": self.__objectType,
            "imageIndex": self.__imageIndex,
            "height": self.__height,
            "width": self.__width,
            "length": self.__length,
            "distance": self.__distance,
            "k_u0": self.__k_u0,
            "k_u1": self.__k_u1,
            "k_v0": self.__k_v0,
            "k_v1": self.__k_v1,
            "k_area": self.__k_area,
            "y_u0": self.__y_u0,
            "y_u1": self.__y_u1,
            "y_v0": self.__y_v0,
            "y_v1": self.__y_v1,
            "y_area": self.__y_area,
            "overlap": self.__overlap,
            "diff_u0": self.__diff_u0,
            "diff_u1": self.__diff_u1,
            "diff_v0": self.__diff_v0,
            "diff_v1": self.__diff_v1
        }

    def buildDataFrame(self):
        self.__buildLists()
        self.__buildDictionary()
        return pd.DataFrame(self.__dictionary)

    @staticmethod
    def saveDataFrame(overlapThreshold, date, splits, verbose=False):
        for split in splits:
            tracklets = TrackletFactory(
                path=os.path.join(ANALYSIS_DIR, date, "mat", f"{split}.mat"),
                verbose=True
            ).tracklets

            detectedObjects = buildDetectedObjectsFromCSV(
                os.path.join(date, "csv", f"{split}_YOLO.csv")
            )

            ctf = CombiTrackletFactory(
                date, split, detectedObjects, tracklets,
                verbose=True, pixelPrecision=10, overlapThreshold=overlapThreshold
            )

            dataFrame = ctf.buildDataFrame()
            file = os.path.join(ANALYSIS_DIR, date, "csv", f"{split}_COMBO_{overlapThreshold}.csv")
            dataFrame.to_csv(file, index=False)

            if verbose:
                print(f"DataFrame Exported: {file}")
