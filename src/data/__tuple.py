from collections import namedtuple

Coordinates = namedtuple("Coordinates", ["x", "y"])
Vertex = namedtuple("Vertex", ["x", "y", "z"])
LidarObjectCoordinates = namedtuple("Obj", ["x", "y"])
PixelCoordinates = namedtuple("PixelCoordinates", ["u", "v"])


Ellipsoid = namedtuple("Ellipsoid", ["a", "f", "b"])
ellipsoid = Ellipsoid(float(6378137), float(1 / 298.257223563), float(6378137 * (1 - 1 / 298.257223563)))

