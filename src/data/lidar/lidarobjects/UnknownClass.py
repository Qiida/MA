from src.data.lidar.LidarObject import LidarObject

COLOR_yellow = (0.9290, 0.6940, 0.1250)


class UnknownClass(LidarObject):
    def __init__(self, data, lidarParameter, color=COLOR_yellow, classification=17):
        super(UnknownClass, self).__init__(data=data,
                                           lidarParameter=lidarParameter,
                                           color=color,
                                           classification=classification)
