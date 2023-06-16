import numpy as np

from src.data.__tuple import LidarObjectCoordinates
from src.data.preparation.computeEgoUTM import computeEgoUTM_ego_egoYaw
from src.data.preparation.computeObjectCenter import computeObjectCenter_x_y
from src.data.preparation.filterNanColumns import filterNanColumns


def computeUTM_ego_obj(data, testVehicle):
    filterNanColumns(data)
    dataObjectLaserRaw = data['object_laser_raw']
    # dataEgo = data['ego']

    ego, egoYaw = computeEgoUTM_ego_egoYaw(ego=data['ego'], testVehicle=testVehicle)

    # objectVelocityAbs, objectVelocityRel = computeObjectVelocity_abs_rel(objectLaserRaw=dataObjectLaserRaw,
    #                                                                      ego=dataEgo)

    objectRefPointX, objectRefPointY = computeObjectCenter_x_y(objectLaserRaw=dataObjectLaserRaw)

    rotAngle = egoYaw / 180 * np.pi

    obj = LidarObjectCoordinates(np.zeros(np.shape(dataObjectLaserRaw['RefPointCoordsX'])), np.zeros(np.shape(dataObjectLaserRaw['RefPointCoordsY'])))
    obj.x.fill(np.nan)
    obj.y.fill(np.nan)

    for i in range(len(dataObjectLaserRaw['objectIDList'])):
        obj.x[:, i] = np.sin(rotAngle) * objectRefPointX[:, i] - np.cos(rotAngle) * objectRefPointY[:, i] + ego.x
        obj.y[:, i] = np.cos(rotAngle) * objectRefPointX[:, i] + np.cos(rotAngle) * objectRefPointY[:, i] + ego.y

    # objectYawRel, objectYawAbs = computeObjectYaw_rel_abs(objectLaserRaw=dataObjectLaserRaw, egoYaw=egoYaw)
    #
    # objectAbsYaw_UZS = -1 * (objectYawAbs - 360)
    # objectYawRate = -1 * dataObjectLaserRaw['ObjYawRate'] * 180 / np.pi

    return ego, obj



