import numpy as np


def angleYaw2utm(longDeg, latDeg, gpsAngleYawDeg, utmZoneNo):
    longCentMeridian = ((utmZoneNo - 30) * 6 - 3) / 180 * np.pi

    longRad = longDeg * np.pi / 180
    latRad = latDeg * np.pi / 180

    meridianKonvergenzDegUtm = np.arctan(np.tan(longCentMeridian - longRad) * np.sin(latRad)) * 180 / np.pi
    gpsAngleYawDegUtm = gpsAngleYawDeg + meridianKonvergenzDegUtm

    return gpsAngleYawDegUtm, meridianKonvergenzDegUtm
