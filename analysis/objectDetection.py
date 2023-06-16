import os

import pandas as pd
from src.data.tracklet.yolo.ObjectDetector import ObjectDetector

PATH = os.path.join("2011_09_26", "2011_09_26_drive_0014_sync")

objectDetector = ObjectDetector(path=PATH, verbose=True)

objectDetector.exportPNG()

dictionary = objectDetector.buildDictionary()

dataFrame = pd.DataFrame(dictionary)




print("The End.")
