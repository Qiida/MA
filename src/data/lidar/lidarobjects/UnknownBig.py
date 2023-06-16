from src.data.lidar.LidarObject import LidarObject

COLOR_darkGrey1 = (0.4, 0.4, 0.4)


class UnknownBig(LidarObject):
    def __init__(self, data, lidarParameter, color=COLOR_darkGrey1, classification=2):
        super(UnknownBig, self).__init__(data=data,
                                         lidarParameter=lidarParameter,
                                         color=color,
                                         classification=classification)
