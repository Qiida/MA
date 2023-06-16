from src.data.lidar.LidarObject import LidarObject

COLOR_purple = (0.4940, 0.1840, 0.5560)


class Truck(LidarObject):
    def __init__(self, data, lidarParameter, color=COLOR_purple, classification=6):
        super(Truck, self).__init__(data=data,
                                    lidarParameter=lidarParameter,
                                    color=color,
                                    classification=classification)
