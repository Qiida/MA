from src.data.lidar.LidarObject import LidarObject

COLOR_blue = (0, 0.4470, 0.7410)


# COLOR_blue = (0, 128, 255)

class Car(LidarObject):
    def __init__(self, data, lidarParameter, color=COLOR_blue, classification=5):
        super(Car, self).__init__(
            data=data,
            lidarParameter=lidarParameter,
            color=color,
            classification=classification
        )
