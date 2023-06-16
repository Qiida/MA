import numpy as np


def computeObjectVelocity_abs_rel(objectLaserRaw, ego):
    objectVelocityAbs = np.sqrt(objectLaserRaw['AbsVelocityX'] ** 2 + objectLaserRaw['AbsVelocityY'] ** 2)
    objectVelocityRel = np.zeros(np.shape(objectVelocityAbs))
    objectVelocityRel.fill(np.nan)

    for objNr in range(len(objectLaserRaw['objectIDList'])):
        objectVelocityRel[:, objNr] = objectVelocityAbs[:, objNr] - ego['vx']

    return objectVelocityAbs, objectVelocityRel

