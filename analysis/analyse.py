import os

from src.data.tracklet.kitti.TrackletFactory import TrackletFactory
from src.data.tracklet.combi.CombiTrackletFactory import CombiTrackletFactory
from src.data.tracklet.yolo.ObjectDetector import buildDetectedObjectsFromCSV
from src.utils.directories import ANALYSIS_DIR

# This script uses all Classes to parse the Kitti-Tracklets and evaluates them with the detected Objects.
# The results are written into a Pandas Data Frame

DATE = "2011_09_26"
SPLIT = "2011_09_26_drive_0014_sync"

# This method builds detected Objects from a CSV file
detectedObjects = buildDetectedObjectsFromCSV(
    os.path.join(ANALYSIS_DIR, DATE, "csv", f"{SPLIT}_YOLO.csv")
)

tf = TrackletFactory(
    path=os.path.join(ANALYSIS_DIR, DATE, "mat", f"{SPLIT}.mat"), verbose=True
)

tracklets = tf.tracklets

ctf = CombiTrackletFactory(
    DATE, SPLIT, detectedObjects, tracklets,
    verbose=True, pixelPrecision=10, overlapThreshold=0.7
)

df = ctf.buildDataFrame()


print("The End.")


