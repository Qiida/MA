import math
from abc import ABC

import numpy as np


class Box(ABC):
    def __init__(self, u, v, imageIndex):
        self.u = u
        self.v = v
        self.imageIndex = imageIndex
        self.area = self.computeArea(u, v)

    @staticmethod
    def computeArea(u, v):
        return abs(u[1] - u[0]) * abs(v[1] - v[0])


class KittiBox(Box):
    def __init__(
            self, u, v, imageIndex, translation, rotation,
            frameSize=(1242, 375)
    ):
        self.frameSize = frameSize
        super().__init__(
            u=self.limit_u(u),
            v=self.limit_v(v),
            imageIndex=imageIndex
        )

        self.translation = translation
        self.rotation = rotation

        self.distance = self.__computeEuclideanDistance()

    def __computeEuclideanDistance(self):
        return math.sqrt(
            pow(self.translation[0], 2) +
            pow(self.translation[1], 2) +
            pow(self.translation[2], 2)
        )

    def limit_u(self, u):
        u0 = u[0]
        u1 = u[1]

        if u[0] > self.frameSize[0]:
            u0 = self.frameSize[0]
        if u[1] > self.frameSize[0]:
            u1 = self.frameSize[0]

        if u[0] < 0:
            u0 = 0
        if u[1] < 0:
            u1 = 0

        return u0, u1

    def limit_v(self, v):
        v0 = v[0]
        v1 = v[1]

        if v[0] > self.frameSize[1]:
            v0 = self.frameSize[1]
        if v[1] > self.frameSize[1]:
            v1 = self.frameSize[1]

        if v[0] < 0:
            v0 = 0
        if v[1] < 0:
            v1 = 0

        return v0, v1



class YoloBox(Box):
    def __init__(self, u, v, imageIndex):
        super().__init__(u=u, v=v, imageIndex=imageIndex)
        self.overlap = None


class EvaluationBox(Box):
    def __init__(self, kBox, yBox=None):
        self.imageIndex = kBox.imageIndex
        self.distance = kBox.distance

        self.k_u = kBox.u
        self.k_v = kBox.v
        self.k_area = kBox.area

        self.y_u = (np.NaN, np.NaN)
        self.y_v = (np.NaN, np.NaN)
        self.y_area = np.NaN

        self.overlap = np.NaN
        self.diff_u = (np.NaN, np.NaN)
        self.diff_v = (np.NaN, np.NaN)

        if yBox is not None:
            self.y_u = yBox.u
            self.y_v = yBox.v
            self.y_area = yBox.area

            self.overlap = yBox.overlap.overlap
            self.diff_u = yBox.overlap.diff_u
            self.diff_v = yBox.overlap.diff_v

        super().__init__(
            u=self.diff_u, v=self.diff_v, imageIndex=self.imageIndex
        )


