import os
import cv2 as cv

from src.utils import loadCalibration, writeCalibration
from src.utils import PROJECTS_DIR, RESOURCES_DIR





if __name__ == '__main__':
    SPLIT = "20191125_IM_1_split_053"
    FRAMES_DIR = os.path.join(PROJECTS_DIR, SPLIT, "images")
    imageFiles = os.listdir(os.path.join(FRAMES_DIR, "../images/gray"))

    mtx, dist = loadCalibration(file=os.path.join(RESOURCES_DIR, "calibration", "calibration.txt"))
    newCameraMatrix = None
    for i, imageFile in enumerate(imageFiles):
        image = cv.imread(os.path.join(FRAMES_DIR, "../images/gray", imageFile))
        h, w = image.shape[:2]

        newCameraMatrix, roi = cv.getOptimalNewCameraMatrix(
            cameraMatrix=mtx,
            distCoeffs=dist,
            imageSize=(h, w),
            alpha=1,
            newImgSize=(h, w)
        )


        # undistorted = cv.undistort(image, mtx, dist, None, newCameraMatrix)
        #
        # x, y, w, h = roi
        # undistorted = undistorted[y:y + h, x:x + w]
        #
        # fileName = os.path.basename(imageFile)
        #
        # undistortedFile = os.path.join(FRAMES_DIR, "../images/undistorted", imageFile)
        # cv.imwrite(undistortedFile, undistorted)
        # print("{} / {} undistorted.".format(f"{i:09d}", f"{len(imageFiles):09d}"))

    writeCalibration(newCameraMatrix, dist, os.path.join(RESOURCES_DIR, "calibration", "calibration_rect.txt"))

    print("Finished.")
