import os

import numpy as np
import pandas
from PIL import Image
from matplotlib import pyplot as plt

from analysis.utils import plotBox
from src.data.tracklet.kitti.TrackletFactory import TrackletFactory
from src.data.tracklet.combi.CombiTrackletFactory import CombiTrackletFactory
from src.data.tracklet.yolo.ObjectDetector import buildDetectedObjectsFromCSV
from src.utils.directories import ANALYSIS_DIR

import matplotlib

matplotlib.use("TkAgg")

DATE = "2011_09_26"
SPLIT = "2011_09_26_drive_0014_sync"

COLOR_KITTI = (1 / 255 * 236, 1 / 255 * 103, 1 / 255 * 27)

df_yolo = pandas.read_csv(os.path.join(ANALYSIS_DIR, DATE, "csv", f"{SPLIT}_YOLO.csv"))
groupByFrame = df_yolo.groupby("imageIndex")
df_combo = pandas.read_csv(os.path.join(ANALYSIS_DIR, DATE, "csv", f"{SPLIT}_COMBO_0.7.csv"))
df_combo = df_combo.filter(
    ["ID", "imageIndex", "overlap", "distance", "k_u0", "k_u1", "k_v0", "k_v1", "y_u0", "y_u1", "y_v0", "y_v1",
     "diff_u0", "diff_u1", "diff_v0", "diff_v1"])
df_grouped = df_combo.groupby(["ID"])
df_110926_0014_2 = df_grouped.get_group("110926_0014_2")

yoloID = 0
for _, row in df_110926_0014_2.iterrows():
    frame = row.imageIndex
    try:
        df_detectedObjects = groupByFrame.get_group(frame)
    except KeyError:
        print(f"{frame} has no detected objects")

    imagePath = os.path.join(ANALYSIS_DIR, DATE, SPLIT, "images", f"{frame:010}.png")
    image = np.asarray(Image.open(imagePath))
    imagePlot = plt.imshow(image)
    figure = plt.gcf()
    axis = plt.gca()

    plotBox(
        ax=axis,
        u=(row.k_u0, row.k_u1),
        v=(row.k_v0, row.k_v1),
        c=COLOR_KITTI,
        lineWidth=1
    )
    ID = int(row.ID.split("_")[-1])
    tag = f"{ID:03d}"
    axis.text(x=row.k_u0, y=row.k_v0 - 5, s=tag, color=COLOR_KITTI, fontfamily="Consolas")

    try:
        for _, yRow in df_detectedObjects.iterrows():
            plotBox(
                ax=axis,
                u=(yRow.u0, yRow.u1),
                v=(yRow.v0, yRow.v1),
                c="red",
                lineWidth=1
            )
            # axis.text(x=yRow.u0, y=yRow.v0 - 5, s=yRow.objectType, color="red", fontfamily="Consolas")
    except:
        print("oh no")
    axis.set_xlim([-2, 1244])
    axis.set_ylim([377, -2])
    plt.axis("off")
    # plt.show()
    plt.savefig(f"combi/{frame:03d}.png", bbox_inches="tight", dpi=1000)
    plt.cla()

    # k_u0 = row.k_u0
    # k_u1 = row.k_u1
    # k_v0 = row.k_v0
    # k_v1 = row.k_v1
    # ID = int(row.ID.split("_")[-1])
    # imagePath = os.path.join(ANALYSIS_DIR, DATE, SPLIT, "images", f"{frame:010}.png")
    # image = np.asarray(Image.open(imagePath))
    # imagePlot = plt.imshow(image)
    # figure = plt.gcf()
    # axis = plt.gca()
    # plotBox(
    #     ax=axis,
    #     u=(k_u0, k_u1),
    #     v=(k_v0, k_v1),
    #     c=COLOR_KITTI,
    #     lineWidth=1
    # )
    # tag = f"{ID:03d}"
    # axis.text(x=k_u0, y=k_v0 - 5, s=tag, color=COLOR_KITTI, fontfamily="Consolas")
    # # figure.set_size_inches(10, 5.625)
    # axis.set_xlim([-2, 1244])
    # axis.set_ylim([377, -2])
    # plt.axis("off")
    # # plt.show()
    # plt.savefig(f"tracklet/110926_0014_2_{frame}.png", bbox_inches="tight", dpi=1000)
    # plt.cla()

print("Wow")
