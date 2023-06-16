from src.data.lidar.LidarObject import LidarObject

COLOR_lightGrey2 = (0.7, 0.7, 0.7)


class UnknownSmall(LidarObject):
    def __init__(self, data, lidarParameter, color=COLOR_lightGrey2, classification=1):
        super(UnknownSmall, self).__init__(data=data,
                                           lidarParameter=lidarParameter,
                                           color=color,
                                           classification=classification)
