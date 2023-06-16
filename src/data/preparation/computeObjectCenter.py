import numpy as np


def computeObjectCenter_x_y(objectLaserRaw):
    refPointLocation = objectLaserRaw['RefPointLocation']
    refPointCoordsX = objectLaserRaw['RefPointCoordsX']
    refPointCoordsY = objectLaserRaw['RefPointCoordsY']
    objCourseAngle = objectLaserRaw['ObjCourseAngle']
    objBoxSizeX = objectLaserRaw['ObjBoxSizeX']
    objBoxSizeY = objectLaserRaw['ObjBoxSizeY']
    objBoxSizeX = objBoxSizeX / 2
    objBoxSizeY = objBoxSizeY / 2

    objCenterX = np.zeros(np.shape(refPointLocation))
    objCenterY = np.zeros(np.shape(refPointLocation))

    objCenterX.fill(np.nan)
    objCenterY.fill(np.nan)
    # =========================================================================
    # '1' # Front / Left
    # =========================================================================
    frontLeft = np.where(refPointLocation == 1)
    objCenterX[frontLeft] = refPointCoordsX[frontLeft] - np.multiply(objBoxSizeX[frontLeft], np.cos(objCourseAngle[frontLeft])) + np.multiply(objBoxSizeY[frontLeft], np.sin(objCourseAngle[frontLeft]))
    objCenterY[frontLeft] = refPointCoordsY[frontLeft] - np.multiply(objBoxSizeX[frontLeft], np.sin(objCourseAngle[frontLeft])) - np.multiply(objBoxSizeY[frontLeft], np.cos(objCourseAngle[frontLeft]))

    # =========================================================================
    # '2' # Front / Right
    # =========================================================================
    frontRight = np.where(refPointLocation == 2)
    objCenterX[frontRight] = refPointCoordsX[frontRight] - np.multiply(objBoxSizeX[frontRight], np.cos(objCourseAngle[frontRight])) - np.multiply(objBoxSizeY[frontRight], np.sin(objCourseAngle[frontRight]))
    objCenterY[frontRight] = refPointCoordsY[frontRight] - np.multiply(objBoxSizeX[frontRight], np.sin(objCourseAngle[frontRight])) + np.multiply(objBoxSizeY[frontRight], np.cos(objCourseAngle[frontRight]))

    # =========================================================================
    # '3' # Rear / Right
    # =========================================================================
    rearRight = np.where(refPointLocation == 3)
    objCenterX[rearRight] = refPointCoordsX[rearRight] + np.multiply(objBoxSizeX[rearRight], np.cos(objCourseAngle[rearRight])) - np.multiply(objBoxSizeY[rearRight], np.sin(objCourseAngle[rearRight]))
    objCenterY[rearRight] = refPointCoordsY[rearRight] + np.multiply(objBoxSizeX[rearRight], np.sin(objCourseAngle[rearRight])) + np.multiply(objBoxSizeY[rearRight], np.cos(objCourseAngle[rearRight]))

    # =========================================================================
    # '4' # Rear / Left
    # =========================================================================
    rearLeft = np.where(refPointLocation == 4)
    objCenterX[rearLeft] = refPointCoordsX[rearLeft] + np.multiply(objBoxSizeX[rearLeft], np.cos(objCourseAngle[rearLeft])) + np.multiply(objBoxSizeY[rearLeft], np.sin(objCourseAngle[rearLeft]))
    objCenterY[rearLeft] = refPointCoordsY[rearLeft] + np.multiply(objBoxSizeX[rearLeft], np.sin(objCourseAngle[rearLeft])) - np.multiply(objBoxSizeY[rearLeft], np.cos(objCourseAngle[rearLeft]))

    # =========================================================================
    # '5' # Front / Center
    # =========================================================================
    frontCenter = np.where(refPointLocation == 5)
    objCenterX[frontCenter] = refPointCoordsX[frontCenter] - np.multiply(objBoxSizeX[frontCenter], np.cos(objCourseAngle[frontCenter]))
    objCenterY[frontCenter] = refPointCoordsY[frontCenter] - np.multiply(objBoxSizeX[frontCenter], np.sin(objCourseAngle[frontCenter]))

    # =========================================================================
    # '6' # Right / Center
    # =========================================================================
    rightCenter = np.where(refPointLocation == 6)
    objCenterX[rightCenter] = refPointCoordsX[rightCenter] - np.multiply(objBoxSizeY[rightCenter], np.sin(objCourseAngle[rightCenter]))
    objCenterY[rightCenter] = refPointCoordsY[rightCenter] + np.multiply(objBoxSizeY[rightCenter], np.cos(objCourseAngle[rightCenter]))

    # =========================================================================
    # '7' # Rear / Center
    # =========================================================================
    rearCenter = np.where(refPointLocation == 7)
    objCenterX[rearCenter] = refPointCoordsX[rearCenter] + np.multiply(objBoxSizeX[rearCenter], np.cos(objCourseAngle[rearCenter]))
    objCenterY[rearCenter] = refPointCoordsY[rearCenter] + np.multiply(objBoxSizeX[rearCenter], np.sin(objCourseAngle[rearCenter]))

    # =========================================================================
    # '8' # Left / Center
    # =========================================================================
    leftCenter = np.where(refPointLocation == 8)
    objCenterX[leftCenter] = refPointCoordsX[leftCenter] + np.multiply(objBoxSizeY[leftCenter], np.sin(objCourseAngle[leftCenter]))
    objCenterY[leftCenter] = refPointCoordsY[leftCenter] - np.multiply(objBoxSizeY[leftCenter], np.cos(objCourseAngle[leftCenter]))

    # =========================================================================
    # '9' # Object Center
    # =========================================================================
    center = np.where(refPointLocation == 9)
    objCenterX[center] = refPointCoordsX[center]
    objCenterY[center] = refPointCoordsY[center]

    # =========================================================================
    # Otherwise
    # =========================================================================
    unknown = np.where((refPointLocation != 1) & (refPointLocation != 2) & (refPointLocation != 3) &
                       (refPointLocation != 4) & (refPointLocation != 5) & (refPointLocation != 6) &
                       (refPointLocation != 7) & (refPointLocation != 8) & (refPointLocation != 9))

    objCenterX[unknown] = np.nan
    objCenterY[unknown] = np.nan

    return objCenterX, objCenterY
