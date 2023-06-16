from abc import ABC

from src.data.tracklet.boxes import EvaluationBox


class Tracklet(ABC):
    def __init__(self, ID, objectType, boxes):
        self.ID = ID
        self.objectType = objectType
        self.boxes = boxes


class KittiTracklet(Tracklet):
    def __init__(self, ID, objectType, boxes, height, width, length, firstFrame, poses):
        super().__init__(ID, objectType, boxes)
        self.height = height
        self.width = width
        self.length = length
        self.firstFrame = firstFrame
        self.poses = poses


class YoloTracklet(Tracklet):
    def __init__(self, ID, objectType, yoloObjects, boxes):
        super().__init__(ID, objectType, boxes)
        self.yoloObjects = yoloObjects


class CombiTracklet(KittiTracklet):
    def __init__(
            self, ID, objectType, height, width, length, firstFrame, poses, kTracklet, kBoxes, yTracklet, yBoxes
    ):

        evaluationBoxes = list()
        for i, kBox in enumerate(kBoxes):
            try:
                yBox = yBoxes[i]
            except IndexError:
                yBox = None
            evaluationBoxes.append(
                EvaluationBox(
                    kBox=kBox,
                    yBox=yBox
                )
            )

        super().__init__(ID, objectType, evaluationBoxes, height, width, length, firstFrame, poses)
        self.kittiTracklet = kTracklet
        self.yoloTracklet = yTracklet
