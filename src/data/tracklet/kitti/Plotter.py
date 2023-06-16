import numpy as np
from matplotlib import pyplot as plt
from src.visualization.EvaluationPlotter import EvaluationPlotter


class KittiPlotter(EvaluationPlotter):
    def __init__(self, path, out, width=0.25, verbose=False, overlapThreshold=0.7):
        super().__init__(path, out, width, verbose, overlapThreshold)

        # private.
        self.__labelLocations = None

    def plotSampleSize(self):
        self.__buildBoxes()
        self.__plotBars()
        self.__setAxis()
        plt.savefig(self.out)

    def __plotBars(self):
        labelLocations = np.arange(10)
        for i, (objectType, boxes) in enumerate(self.boxes.items()):
            offset = self.width * i
            rectangles = self.axis.bar(
                labelLocations + offset,
                boxes,
                self.width,
                label=objectType
            )


    def __setAxis(self):
        labelLocations = np.arange(10)
        xTicks = [
            "> 0",
            "> 10",
            "> 20",
            "> 30",
            "> 40",
            "> 50",
            "> 60",
            "> 70",
            "> 80",
            "> 90"
        ]
        self.axis.set_xlabel("Distanz [m]")
        self.axis.set_ylabel("Boxen [-]")
        self.axis.set_xticks(labelLocations + self.width, xTicks)
        self.axis.legend(self.objectTypes)


    def __buildBoxes(self):
        df = self.giantDataFrame.filter(
            items=["objectType", "distance", "distanceClass"]
        )

        df = df.groupby(
            ["objectType", "distanceClass"],
            as_index=False
        ).count()

        self.boxes = dict()
        for objectType in self.objectTypes:
            numberOfBoxes = [0] * 10
            i = 0

            for index, row in df.iterrows():
                if row.objectType == objectType:
                    numberOfBoxes[i] = row.distance
                    i += 1

            self.boxes.update(
                {
                    objectType: numberOfBoxes
                }
            )


