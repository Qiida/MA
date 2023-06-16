import os

import numpy as np
import pandas as pd
from PIL import Image
from matplotlib import pyplot as plt

from src.data.tracklet.kitti.TrackletFactory import TrackletFactory
from src.data.tracklet.combi.CombiTrackletFactory import CombiTrackletFactory
from src.data.tracklet.yolo.ObjectDetector import buildDetectedObjectsFromCSV
from src.utils.directories import ANALYSIS_DIR

import matplotlib

matplotlib.use("TkAgg")

DATE = "2011_09_26"
SPLIT = "2011_09_26_drive_0013_sync"
FRAMES = [60, 61, 72, 73, 74, 75]
P = 10
O = 0.8

detectedObjects = buildDetectedObjectsFromCSV(
    os.path.join(DATE, "csv", f"{SPLIT}_YOLO.csv")
)

tf = TrackletFactory(
    path=os.path.join(ANALYSIS_DIR, DATE, "mat", f"{SPLIT}.mat"), verbose=True
)

tracklets = tf.tracklets

ctf = CombiTrackletFactory(
    DATE, SPLIT, detectedObjects, tracklets,
    verbose=True, pixelPrecision=P, overlapThreshold=O
)

df = ctf.buildDataFrame()
df = df.filter(
    ["ID", "imageIndex", "overlap", "distance", "k_u0", "k_u1", "k_v0", "k_v1", "y_u0", "y_u1", "y_v0", "y_v1",
     "diff_u0", "diff_u1", "diff_v0", "diff_v1"])

df_grouped = df.groupby(["ID"])
df_110926_0013_0 = df_grouped.get_group("110926_0013_0")
# for _, row in df_110926_0014_2.iterrows():
df_110926_0013_0.set_index("imageIndex", inplace=True)
a = df_110926_0013_0.filter(["distance", "overlap", "diff_u0", "diff_u1", "diff_v0", "diff_v1"])
for frame in FRAMES:
    row = df_110926_0013_0.loc[frame]

    k_u0 = row.k_u0
    k_u1 = row.k_u1
    k_v0 = row.k_v0
    k_v1 = row.k_v1

    y_u0 = row.y_u0
    y_u1 = row.y_u1
    y_v0 = row.y_v0
    y_v1 = row.y_v1


    def plotBox(ax, u, v, c):
        ax.plot((u[0], u[0]), (v[0], v[1]), c=c, linewidth=2)
        ax.plot((u[0], u[1]), (v[1], v[1]), c=c, linewidth=2)
        ax.plot((u[1], u[1]), (v[1], v[0]), c=c, linewidth=2)
        ax.plot((u[1], u[0]), (v[0], v[0]), c=c, linewidth=2)


    imagePath = os.path.join(ANALYSIS_DIR, DATE, SPLIT, "images", f"{frame:010}.png")
    image = np.asarray(Image.open(imagePath))
    imagePlot = plt.imshow(image)
    axis = plt.gca()
    plotBox(
        ax=axis,
        u=(k_u0, k_u1),
        v=(k_v0, k_v1),
        c=(1 / 255 * 236, 1 / 255 * 103, 1 / 255 * 27)
    )
    if not np.isnan(row.overlap):
        plotBox(
            ax=axis,
            u=(y_u0, y_u1),
            v=(y_v0, y_v1),
            c="green"
        )

    # axis.set_xlim([470, 725])
    # axis.set_ylim([230, 140])
    axis.set_xlim([530, 630])
    axis.set_ylim([260, 160])
    # plt.show()
    plt.axis("off")
    plt.savefig(f"110926_0013_0_{frame}_p{P}_o{O}_boxes.png", bbox_inches="tight", dpi=1000)
    plt.cla()
print("The End.")
