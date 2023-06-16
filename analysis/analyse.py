import os

from src.data.tracklet.kitti.TrackletFactory import TrackletFactory
from src.data.tracklet.combi.CombiTrackletFactory import CombiTrackletFactory
from src.data.tracklet.yolo.ObjectDetector import buildDetectedObjectsFromCSV
from src.utils.directories import ANALYSIS_DIR

DATE = "2011_09_26"
SPLIT = "2011_09_26_drive_0014_sync"


detectedObjects = buildDetectedObjectsFromCSV(
    os.path.join(DATE, "csv", f"{SPLIT}_YOLO.csv")
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


