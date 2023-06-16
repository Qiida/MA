from src.data.lidar.boundingBox.BoundingBox import BoundingBox


class TestVehicle:
    def __init__(self, vehicleType):
        self.wheelbase = None
        self.steering_ratio = None
        self.rotation_inertia = None
        self.cog = None
        self.wheelbase_rear = None
        self.mass = None
        self.cavc = None
        self.cav = None
        self.cah = None
        self.cl = None
        self.nv = None
        self.imu_offset_x = None
        self.imu_offset_y = None
        self.imu_offset_z = None
        self.rearaxle_to_front = None
        self.rearaxle_to_rear = None
        self.rdr_offset_x = None
        self.rdr_offset_y = None
        self.rdr_offset_z = None
        self.length = None
        self.width = None
        self.height = None
        self.turningcircle = None

        self.boundingBox = None

        self.__initialize(vehicleType)

    def __buildBoundingBox(self):
        return BoundingBox(width=self.width,
                           length=self.length,
                           height=self.height,
                           color="black",
                           lineWidth=2,
                           isTestVehicle=True,
                           rearAxleToFront=self.rearaxle_to_front,
                           rearAxleToRear=self.rearaxle_to_rear)

    def __initialize(self, vehicleType):
        match vehicleType:
            case "TEASY3":
                self.__initializeTEASY3()
            case "TIAMO":
                self.__initializeTIAMO()
            case "OFFICE":
                self.__initializeOFFICE()

        self.boundingBox = self.__buildBoundingBox()

    def __initializeTEASY3(self):
        self.wheelbase = 2.789  # m
        self.steering_ratio = 15.25  # -
        self.rotation_inertia = 3400  # kgm^2
        self.cog = 0.4  # -
        self.wheelbase_rear = self.wheelbase * (1 - self.cog)  # m
        self.mass = 1900  # kg
        self.cavc = 100000  # N/rad
        self.cav = 100000  # N/rad
        self.cah = 110000  # N/rad
        self.cl = 25000  # Nm/rad
        self.nv = 0.05  # m
        self.imu_offset_x = 1.500  # m
        self.imu_offset_y = -0.450  # m
        self.imu_offset_z = 1.530  # m
        self.rearaxle_to_front = 3.653  # m
        self.rearaxle_to_rear = 1.118  # m
        self.rdr_offset_x = 3.60  # m
        self.rdr_offset_y = 0  # m
        self.rdr_offset_z = 0  # m
        self.length = 4.777  # m
        self.width = 1.832  # m
        self.height = 1.850  # m
        self.turningcircle = 11.7  # m

    def __initializeTIAMO(self):
        self.wheelbase = 2.630
        self.steering_ratio = 14.2
        self.rotation_inertia = 3400
        self.cog = 0.53
        self.wheelbase_rear = self.wheelbase * (1 - self.cog)
        self.mass = 1600
        self.cavc = 70000
        self.cav = 100000
        self.cah = 110000
        self.cl = 25000
        self.nv = 0.05
        self.imu_offset_x = 0.733
        self.imu_offset_y = 0.285
        self.imu_offset_z = 1.460
        self.rearaxle_to_front = 3.492
        self.rearaxle_to_rear = 0.763
        self.rdr_offset_x = 3.30
        self.rdr_offset_y = 0
        self.rdr_offset_z = 0
        self.length = 4.255
        self.width = 1.799
        self.height = 1.900
        self.turningcircle = 10.95

    def __initializeOFFICE(self):
        self.wheelbase = 2.630
        self.steering_ratio = 14.2
        self.rotation_inertia = 3400
        self.cog = 0.53
        self.wheelbase_rear = self.wheelbase * (1 - self.cog)
        self.mass = 1600
        self.cavc = 70000
        self.cav = 100000
        self.cah = 110000
        self.cl = 25000
        self.nv = 0.05
        self.imu_offset_x = 0.733
        self.imu_offset_y = 0.285
        self.imu_offset_z = 1.460
        self.rearaxle_to_front = 3.653
        self.rearaxle_to_rear = 1.118
        self.rdr_offset_x = 3.30
        self.rdr_offset_y = 0
        self.rdr_offset_z = 0
        self.length = 4.255
        self.width = 1.799
        self.height = 1.900
        self.turningcircle = 10.95





