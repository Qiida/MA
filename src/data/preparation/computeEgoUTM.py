import numpy as np

from src.data.__tuple import Coordinates
from src.data.preparation.angleYaw2utm import angleYaw2utm
from src.data.preparation.deg2utm import deg2utm


def computeEgoUTM_ego_egoYaw(ego, testVehicle):
    longAbs = ego['long_abs']
    latAbs = ego['lat_abs']
    gpsAngleYaw = ego['GPS_Angle_Yaw']

    UTM_LONG, UTM_LAT, UTM_ZONE_No, UTM_ZONE_Char = deg2utm(longAbs, latAbs)
    egoYaw, _ = angleYaw2utm(longAbs, latAbs, gpsAngleYaw, UTM_ZONE_No)

    ego = Coordinates(UTM_LONG - np.sin(np.deg2rad(egoYaw)) * testVehicle.imu_offset_x + np.cos(
        np.deg2rad(egoYaw)) * testVehicle.imu_offset_y, UTM_LAT - np.cos(np.deg2rad(egoYaw)) * testVehicle.imu_offset_x
                      - np.sin(np.deg2rad(egoYaw)) * testVehicle.imu_offset_y)

    return ego, egoYaw
