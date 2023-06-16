from src.data.lidar.LidarObject import LidarObject

COLOR_lightGrey1 = (0.85, 0.85, 0.85)


class NotClassified(LidarObject):
    def __init__(self, data, lidarParameter, color=COLOR_lightGrey1, classification=0):
        super(NotClassified, self).__init__(data=data,
                                            lidarParameter=lidarParameter,
                                            color=color,
                                            classification=classification)
