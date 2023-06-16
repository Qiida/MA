import os

from src.data.tracklet.boxes import KittiBox
from src.data.tracklet.matlabfile import MatlabFile
from src.data.tracklet.tracklets import KittiTracklet


class TrackletFactory:
    def __init__(
            self, path, verbose=False, classesOfInterest=None,
            frameSize=(1242, 375)
    ):
        self.verbose = verbose
        self.frameSize = frameSize

        # public.
        self.path = path
        self.name = os.path.basename(self.path).split(".")[0]
        self.tracklets = None

        # private.
        self.__ID = None
        self.__u0 = None
        self.__u1 = None
        self.__v0 = None
        self.__v1 = None
        self.__distance = None
        self.__area = None
        self.__objectType = None
        self.__imageIndex = None
        self.__files = None

        self.__initialize(classesOfInterest)
        self.__buildTracklets()


    def __initialize(self, classesOfInterest):

        if classesOfInterest is None:
            self.classesOfInterest = [
                "Car",
                "Truck",
                "Van",
                "Tram",
                "Pedestrian",
                "Person (Sitting)",
                "Misc",
                "Cyclist"
            ]
        else:
            self.classesOfInterest = classesOfInterest

        self.__files = list()

        if os.path.isdir(self.path):
            if self.verbose:
                print("Build from dir: {}".format(self.path))
            self.__loadMatFiles()

        if os.path.isfile(self.path):
            if self.verbose:
                print("Build from path: {}".format(self.path))

            self.__files.append(
                MatlabFile(path=self.path)
            )

    def buildDictionary(self):
        self.__buildLists()
        dictionary = {
            "ID": self.__ID,
            "objectType": self.__objectType,
            "imageIndex": self.__imageIndex,
            "u0": self.__u0,
            "u1": self.__u1,
            "v0": self.__v0,
            "v1": self.__v1,
            "area": self.__area,
            "distance": self.__distance
        }
        return dictionary

    def __buildTracklets(self):
        self.tracklets = []

        for file in self.__files:
            if self.verbose:
                print(f"\n\n[{file.dataSetName}]")

            data = file.data
            dataSetShortName = file.dataSetShortName
            for i, tracklet_raw in enumerate(data["export"]["tracklets"]):
                try:
                    boxes = []
                    if self.__isOfInterest(tracklet_raw.objectType):
                        for box_raw in tracklet_raw.boxes:
                            box = self.buildKittiBox(box_raw)
                            if not (box.u == (0, self.frameSize[0]) and (box.v == (0, self.frameSize[1]))):
                                boxes.append(
                                    box
                                )

                        self.tracklets.append(
                            KittiTracklet(
                                ID=dataSetShortName + "_" + str(i),
                                objectType=tracklet_raw.objectType,
                                height=tracklet_raw.h,
                                length=tracklet_raw.l,
                                firstFrame=tracklet_raw.first_frame,
                                width=tracklet_raw.w,
                                poses=tracklet_raw.poses,
                                boxes=boxes
                            )
                        )
                except TypeError:
                    print(f"Error building Tracklet: {i}")



    @staticmethod
    def buildKittiBox(box_raw):
        box = KittiBox(
            u=(box_raw.x1, box_raw.x2),
            v=(box_raw.y1, box_raw.y2),
            imageIndex=box_raw.img_idx,
            translation=box_raw.pose.t,
            rotation=box_raw.pose.rz
        )
        return box

    def __isOfInterest(self, objectType):
        for classOfInterest in self.classesOfInterest:
            if classOfInterest == objectType:
                return True
        return False

    def __buildLists(self):
        self.__ID = []
        self.__objectType = []
        self.__imageIndex = []
        self.__u0 = []
        self.__u1 = []
        self.__v0 = []
        self.__v1 = []
        self.__area = []
        self.__distance = []

        for tracklet in self.tracklets:

            if self.__isOfInterest(tracklet.objectType):
                for box in tracklet.boxes:
                    self.__ID.append(tracklet.ID)
                    self.__objectType.append(tracklet.objectType)
                    self.__imageIndex.append(box.imageIndex)
                    self.__u0.append(box.u[0])
                    self.__u1.append(box.u[1])
                    self.__v0.append(box.v[0])
                    self.__v1.append(box.v[1])
                    self.__area.append(box.area)
                    self.__distance.append(box.distance)

    def __loadMatFiles(self):
        fileList = os.listdir(self.path)
        for file in fileList:
            if self.verbose:
                print(file)
            try:
                if file.split(".")[1] == "mat":
                    self.__files.append(
                        MatlabFile(path=os.path.join(self.path, file))
                    )
            except IndexError:
                pass
