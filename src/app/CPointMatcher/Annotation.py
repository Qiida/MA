from enum import Enum


class AnnotationStyle(Enum):
    LAYOUT = 1
    POINTS = 2


class Annotation:

    def __init__(self, frameNr, points):
        self.frameNr = frameNr
        self.points = points
