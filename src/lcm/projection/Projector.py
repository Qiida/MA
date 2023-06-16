import numpy as np


class Projector:
    def __init__(self, intrinsic, extrinsic, verbose=False):
        self.verbose = verbose
        self.extrinsic = None
        self.intrinsic = None
        self.projectionMatrix = None
        self.initializeMatrices(intrinsic, extrinsic)

    def initializeMatrices(self, intrinsic, extrinsic):
        self.initializeIntrinsic(intrinsic)
        self.initializeExtrinsic(extrinsic)
        self.initializeProjectionMatrix()

    def initializeProjectionMatrix(self):
        self.projectionMatrix = np.matmul(self.intrinsic, self.extrinsic)

    def initializeExtrinsic(self, extrinsic):
        self.extrinsic = np.zeros((4, 4))
        for i in range(3):
            for j in range(3):
                try:
                    self.extrinsic[i][j] = extrinsic[i][j]
                except IndexError:
                    pass
        self.extrinsic[0][3] = extrinsic[0][3]
        self.extrinsic[1][3] = extrinsic[1][3]
        self.extrinsic[2][3] = extrinsic[2][3]
        self.extrinsic[3][3] = 1
        if self.verbose:
            print(f"\n[extrinsic]\n{self.extrinsic}")

    def initializeIntrinsic(self, intrinsic):
        self.intrinsic = np.zeros((3, 4))
        for i in range(3):
            for j in range(4):
                try:
                    self.intrinsic[i][j] = intrinsic[i][j]
                except IndexError:
                    pass
                except TypeError:
                    print("TypeError")
        if self.verbose:
            print(f"\n[intrinsic]\n{self.intrinsic}")

    def project(self, objectPoint):
        vector = self.__createObjectPointVector(objectPoint)
        projected = np.matmul(self.projectionMatrix, vector)
        return projected / projected[2]


    @staticmethod
    def __createObjectPointVector(objectPoint):
        _objectPoint = np.zeros(4)
        for i in range(3):
            _objectPoint[i] = objectPoint[i]
            _objectPoint[3] = 1
        return _objectPoint


