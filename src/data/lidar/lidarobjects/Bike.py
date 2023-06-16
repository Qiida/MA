from src.data.lidar.LidarObject import LidarObject

COLOR_orange = (0.8500, 0.3250, 0.0980)


class Bike(LidarObject):
    def __init__(self, data, lidarParameter, color=COLOR_orange, classification=4):
        super(Bike, self).__init__(data=data,
                                   lidarParameter=lidarParameter,
                                   color=color,
                                   classification=classification)
