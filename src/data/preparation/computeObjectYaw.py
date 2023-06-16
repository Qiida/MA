import numpy as np


def computeObjectYaw_rel_abs(objectLaserRaw, egoYaw):
    objectYawRel = np.mod(objectLaserRaw['ObjCourseAngle'] * 180 / np.pi, 360)
    objectYawAbs = np.zeros(np.shape(objectYawRel))
    objectYawAbs.fill(np.nan)

    for i in range(len(objectLaserRaw['objectIDList'])):
        try:
            objectYawAbs[:, i] = np.mod(objectYawRel[:, i] - egoYaw, 360)
        except TypeError:
            print("{} print Error".format(i))

    return objectYawRel, objectYawAbs
