import os

import pandas as pd

from src.data.tracklet.kitti.TrackletFactory import TrackletFactory
from src.data.tracklet.yolo.ObjectDetector import ObjectDetector

from src.utils.directories import ANALYSIS_DIR

DATE = "2011_09_26"
SPLITS = [
    "2011_09_26_drive_0001_sync",
    "2011_09_26_drive_0002_sync",
    "2011_09_26_drive_0005_sync",
    "2011_09_26_drive_0009_sync",
    "2011_09_26_drive_0011_sync",
    "2011_09_26_drive_0013_sync",
    "2011_09_26_drive_0014_sync",
    "2011_09_26_drive_0015_sync",
    "2011_09_26_drive_0017_sync",
    "2011_09_26_drive_0019_sync",
    "2011_09_26_drive_0020_sync",
    "2011_09_26_drive_0022_sync",
    "2011_09_26_drive_0023_sync",
    "2011_09_26_drive_0027_sync",
    "2011_09_26_drive_0028_sync",
    "2011_09_26_drive_0029_sync",
    "2011_09_26_drive_0032_sync",
    "2011_09_26_drive_0035_sync",
    "2011_09_26_drive_0036_sync",
    "2011_09_26_drive_0039_sync",
    "2011_09_26_drive_0046_sync",
    "2011_09_26_drive_0051_sync",
    "2011_09_26_drive_0052_sync",
    "2011_09_26_drive_0056_sync",
    "2011_09_26_drive_0057_sync",
    "2011_09_26_drive_0059_sync",
    "2011_09_26_drive_0060_sync",
    "2011_09_26_drive_0064_sync",
    "2011_09_26_drive_0070_sync",
    "2011_09_26_drive_0079_sync",
    "2011_09_26_drive_0086_sync",
    "2011_09_26_drive_0087_sync",
    "2011_09_26_drive_0091_sync",
    "2011_09_26_drive_0093_sync"
]


trackletFactories = []
objectDetectors = []
for split in SPLITS:
    trackletFactories.append(
        TrackletFactory(path=os.path.join(ANALYSIS_DIR, DATE, "mat", f"{split}.mat"), verbose=True)
    )
    objectDetectors.append(
        ObjectDetector(path=os.path.join(ANALYSIS_DIR, DATE, f"{split}"), verbose=True)
    )

# objectDetectors[0].writeVideo()

for tf in trackletFactories:
    df = pd.DataFrame(tf.buildDictionary())
    df.to_csv(os.path.join(DATE, "csv", f"{tf.name}.csv"), index=False)
    print(f"Exported: {tf.name}.csv")

for od in objectDetectors:
    df = pd.DataFrame(od.buildDictionary())
    od.exportPNG()
    df.to_csv(os.path.join(DATE, "csv", f"{od.name}_YOLO.csv"), index=False)

print("The End.")
