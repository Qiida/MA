from src.data.lidar.LidarObject import LidarObject

COLOR_green = (0.4660, 0.6740, 0.1880)


class Pedestrian(LidarObject):
    def __init__(self, data, lidarParameter, color=COLOR_green, classification=3):
        super(Pedestrian, self).__init__(data=data,
                                         lidarParameter=lidarParameter,
                                         color=color,
                                         classification=classification)
