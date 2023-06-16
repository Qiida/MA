from src.app.CPointMatcher.CorrespondencePointMatcher import extractPointPairs


class PointPair:
    def __init__(self, idNr, imagePoint, objectPoint):
        self.idNr = idNr
        self.imagePoint = imagePoint
        self.objectPoint = objectPoint


class PointPairFabric:
    def __init__(self, file, lidarObjects):
        self.file = file
        self.lidarObjects = lidarObjects
        self.imagePoints = []
        self.objectPoints = []


        imgPts, objPts = extractPointPairs(correspondencePointsFile=self.file, lidarObjects=self.lidarObjects)
        self.imagePoints = imgPts
        self.objectPoints = objPts

