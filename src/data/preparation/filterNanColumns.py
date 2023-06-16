import numpy as np


def filterNanColumns(data):
    objectLaserRaw = data["object_laser_raw"]
    objectIDList = data["object_laser_raw"]["objectIDList"]

    isEmptyCol = np.zeros(len(objectIDList), dtype="uint8")
    classification = np.float16(objectLaserRaw["Classification"])

    for objNr in range(len(objectIDList)):
        isEmptyCol[objNr] = np.all(np.isnan(classification[:, objNr]))

    if np.sum(isEmptyCol) > 0:
        emptyCol = np.where(isEmptyCol == 1)
        keys = list(objectLaserRaw.keys())

        for key in keys:
            if key != "time_can":
                objectLaserRaw[key] = objectLaserRaw[key][:, ~np.isnan(objectLaserRaw[key]).all(axis=0)]

        data["object_laser_raw"]["objectIDList"] = np.uint8(np.delete(objectIDList, emptyCol, axis=0))