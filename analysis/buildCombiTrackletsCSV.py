from src.data.tracklet.combi.CombiTrackletFactory import CombiTrackletFactory

OVERLAP_THRESHOLDS = [
    0.3,
    # 0.4,
    # 0.5,
    # 0.6,
    # 0.7,
    0.8,
    # 0.9
]
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

for OVERLAP_THRESHOLD in OVERLAP_THRESHOLDS:
    CombiTrackletFactory.saveDataFrame(
        overlapThreshold=OVERLAP_THRESHOLD,
        date=DATE,
        splits=SPLITS,
        verbose=True
    )

print(f"[Finished.]")