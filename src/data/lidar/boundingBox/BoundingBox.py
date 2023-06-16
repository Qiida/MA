import matplotlib
import matplotlib.pyplot as plt
import numpy as np

from src.data.__tuple import Coordinates, Vertex

matplotlib.use("TkAgg")


def buildRotationMatrix(courseAngle):
    rotationMatrix = np.empty(shape=(2, 2))
    rotationMatrix[0][0] = np.cos(courseAngle)
    rotationMatrix[0][1] = -np.sin(courseAngle)
    rotationMatrix[1][0] = np.sin(courseAngle)
    rotationMatrix[1][1] = np.cos(courseAngle)
    return rotationMatrix


def rotate(x, y, courseAngle):
    xy = np.transpose(np.array([x, y]))
    rotationMatrix = buildRotationMatrix(courseAngle)
    xy = np.matmul(rotationMatrix, xy)
    return xy[0], xy[1]


def translate(x, y, coordinates):
    return x + coordinates[0], y + coordinates[1]


class BoundingBox:

    def __init__(self, width, length, height, color, lineWidth, lidarObject=None,
                 isTestVehicle=False, rearAxleToFront=None, rearAxleToRear=None):

        # Public.
        self.lidarObject = lidarObject
        self.width = width
        self.length = length
        self.height = height
        self.color = color
        self.lineWidth = lineWidth
        self.isTestVehicle = isTestVehicle
        # TODO: Build all Vertices, so they can later be easily be accessed.

        # Private.
        self.__rearAxleToFront = None
        self.__rearAxleToBack = None

        self.__initialize(isTestVehicle, rearAxleToFront, rearAxleToRear)

    def getAllVertices(self):
        coordinates = self.lidarObject.coordinates
        courseAngle = self.lidarObject.courseAngle
        dimensions = (courseAngle.size, 8)

        vertices = self.__initializeVertices(dimensions)

        for idNr in range(dimensions[0]):
            for vertex in range(dimensions[1]):
                coordinates_idNr = (coordinates[idNr][0], coordinates[idNr][1])
                vertices[idNr][vertex] = self.__buildVertex(vertex, coordinates_idNr, courseAngle[idNr])
        return vertices

    def getCornersFromIdNr(self, idNr):
        index = self.lidarObject.getIndex(idNr)
        coordinates = self.lidarObject.coordinates[index]
        vertices = list()
        for v in range(8):
            vertices.append(self.__buildVertex(v, coordinates, self.lidarObject.courseAngle[index]))
        return np.array(vertices, dtype=np.float32)

    def getTransformedImagePoints(self, idNr, intrinsic, extrinsic):
        vertices = self.getCornersFromIdNr(idNr)
        transformed = []

        vertex = np.zeros(4)
        for v in range(8):
            _vertices = vertices[v]
            for i in range(3):
                vertex[i] = _vertices[i]

            vertex[3] = 1
            p = np.matmul(intrinsic, extrinsic)

            _transformed = np.matmul(p, vertex)
            transformed.append(_transformed / _transformed[2])

        return np.array(transformed)

    def __initialize(self, isTestVehicle, rearAxleToFront, rearAxleToRear):
        if isTestVehicle:
            if rearAxleToFront is None or rearAxleToRear is None:
                raise AttributeError
            self.__rearAxleToFront = rearAxleToFront
            self.__rearAxleToBack = rearAxleToRear

    def draw(self, axis, coordinates=Coordinates(x=0, y=0), courseAngle=0):
        self.__buildVertices_temp(coordinates, courseAngle)
        self.__drawBoundingBox(axis)
        self.__drawID(axis)

    def getVertices(self, coordinates=Coordinates(x=0, y=0), courseAngle=0):
        self.__buildVertices_temp(coordinates, courseAngle)
        return self.vertices_temp

    def __buildVertices_temp(self, coordinates, courseAngle):
        self.__initializeVertices_temp()

        for vertex in range(self.vertices_temp.size):
            self.vertices_temp[vertex] = self.__buildVertex(vertex, coordinates, courseAngle)

        return self.vertices_temp

    @staticmethod
    def __initializeVertices(dimensions):
        return np.empty(dimensions, dtype=object)

    def __initializeVertices_temp(self):
        self.vertices_temp = np.empty(8, dtype=object)

    def __buildVertex(self, vertex, coordinates, courseAngle):

        x, y, z = self.__getXYZ(vertex)
        x, y = rotate(x, y, courseAngle)
        x, y = translate(x, y, coordinates)

        return x, y, z

    def __getXYZ(self, vertex):
        x, y, z = None, None, None
        match vertex:
            case 0:
                if self.isTestVehicle:
                    x = - self.__rearAxleToBack
                else:
                    x = - self.length / 2
                y = + self.width / 2
                z = 0
            case 1:
                if self.isTestVehicle:
                    x = + self.__rearAxleToFront
                else:
                    x = + self.length / 2
                y = + self.width / 2
                z = 0
            case 2:
                if self.isTestVehicle:
                    x = self.__rearAxleToFront
                else:
                    x = + self.length / 2
                y = - self.width / 2
                z = 0
            case 3:
                if self.isTestVehicle:
                    x = - self.__rearAxleToBack
                else:
                    x = - self.length / 2
                y = - self.width / 2
                z = 0
            case 4:
                if self.isTestVehicle:
                    x = - self.__rearAxleToBack
                else:
                    x = - self.length / 2
                y = + self.width / 2
                z = self.height
            case 5:
                if self.isTestVehicle:
                    x = self.__rearAxleToFront
                else:
                    x = + self.length / 2
                y = + self.width / 2
                z = self.height
            case 6:
                if self.isTestVehicle:
                    x = self.__rearAxleToFront
                else:
                    x = + self.length / 2
                y = - self.width / 2
                z = self.height
            case 7:
                if self.isTestVehicle:
                    x = - self.__rearAxleToBack
                else:
                    x = - self.length / 2
                y = - self.width / 2
                z = self.height
        return x, y, z

    def __drawBoundingBox(self, axis):
        self.__drawLine(axis, self.vertices_temp[0], self.vertices_temp[1])
        self.__drawLine(axis, self.vertices_temp[1], self.vertices_temp[2])
        self.__drawLine(axis, self.vertices_temp[2], self.vertices_temp[3])
        self.__drawLine(axis, self.vertices_temp[3], self.vertices_temp[0])

        self.__drawLine(axis, self.vertices_temp[0], self.vertices_temp[4])
        self.__drawLine(axis, self.vertices_temp[1], self.vertices_temp[5])
        self.__drawLine(axis, self.vertices_temp[2], self.vertices_temp[6])
        self.__drawLine(axis, self.vertices_temp[3], self.vertices_temp[7])

        self.__drawLine(axis, self.vertices_temp[4], self.vertices_temp[5])
        self.__drawLine(axis, self.vertices_temp[5], self.vertices_temp[6])
        self.__drawLine(axis, self.vertices_temp[6], self.vertices_temp[7])
        self.__drawLine(axis, self.vertices_temp[7], self.vertices_temp[4])

    def __drawLine(self, axis, startpoint, endpoint, color=None):
        if color is None:
            color = self.color
        x, y, z = [startpoint[0], endpoint[0]], [startpoint[1], endpoint[1]], [startpoint[2], endpoint[2]]
        axis.plot(x, y, z, color=color, linewidth=self.lineWidth)

    def __drawID(self, axis):
        try:
            if self.lidarObject.ID is not None:
                v0 = self.vertices_temp[0][0]
                v1 = self.vertices_temp[0][1]
                v2 = self.vertices_temp[0][2]
                try:
                    a = int(v0)
                    b = int(v1)
                    c = int(v2)
                    axis.text(self.vertices_temp[0][0], self.vertices_temp[0][1], self.vertices_temp[0][2],
                              str(self.lidarObject.ID))
                except:
                    print("Error BoundingBox__drawID: ID: {}".format(self.lidarObject.ID))
        except AttributeError:
            pass



if __name__ == '__main__':
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    ax.axis("auto")
    ax.set_xlabel("x")
    ax.set_ylabel("y")

    bBox = BoundingBox(width=2, length=5, height=1.5, color="red", lineWidth=2)
    bBox.draw(ax, coordinates=Coordinates(1, 2), courseAngle=45)
    plt.show()
