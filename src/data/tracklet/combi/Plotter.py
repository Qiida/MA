import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
from scipy.interpolate import InterpolatedUnivariateSpline

from src.data.tracklet.TrackletAnalyser import TrackletAnalyser
from src.visualization.EvaluationPlotter import EvaluationPlotter

import matplotlib

matplotlib.use("TkAgg")


class TrackletPlotter(EvaluationPlotter):
    def __init__(self, path, out, verbose=False, overlapThreshold=0.8, trackletFilter=None):
        super().__init__(path, out, verbose, overlapThreshold)
        self.trackletsThatGotLost = None
        self.save = None
        self.closingIn = None
        self.drivingAway = None
        self.distanceClasses = (
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
        )

        if trackletFilter is None:
            self.trackletFilter = []
        else:
            self.trackletFilter = trackletFilter

        self.__buildTracklets()
        self.__buildDataFrame()

    def __buildTracklets(self):
        df = self.giantDataFrame.filter(
            items=[
                "ID",
                "objectType",
                "distance",
                "distanceClass",
                "k_area",
                "imageIndex",
                "matched"
            ]
        )
        _filter = df["objectType"] == "Car"
        df = df[_filter]

        self.trackletAnalysers = dict()
        for trackletID in df.ID.unique():
            trackletDF = df.groupby("ID").get_group(trackletID)
            self.trackletAnalysers.update(
                {
                    trackletID: TrackletAnalyser(trackletDF)
                }
            )

        ID = []
        found = []
        lost = []

        for tracklet in self.trackletAnalysers.values():
            ID.append(tracklet.ID)
            if len(tracklet.found) > 0:
                found.append(tracklet.found[0])
            else:
                found.append(None)
            if len(tracklet.lost) > 0:
                lost.append(tracklet.lost[0])
            else:
                lost.append(None)

        dictionary = {
            "ID": ID,
            "found": found,
            "lost": lost
        }

        self.trackletsThatGotLost = []
        if len(self.trackletFilter) > 0:
            self.trackletsThatGotLost = self.trackletFilter

        else:
            lostAndFoundDf = pd.DataFrame(dictionary)
            for _, row in lostAndFoundDf.iterrows():
                if row.lost > row.found or row.lost < row.found:
                    self.trackletsThatGotLost.append(row.ID)

    def scatterPlotTracklets(self, save=True, xLim=None, yLim=None):
        self.save = save

        for trackletThatGotLost in self.trackletsThatGotLost:
            tracklet = self.trackletAnalysers.get(trackletThatGotLost)

            xFound = tracklet.foundFrame
            yFound = tracklet.found

            xLost = tracklet.lostFrame
            yLost = tracklet.lost

            found = self.axis.scatter(
                x=xFound,
                y=yFound,
                c="b",
                s=40,
                marker="."
            )

            lost = self.axis.scatter(
                x=xLost,
                y=yLost,
                c="r",
                s=20,
                marker="x"
            )
            self.axis.set_xlabel("Frame [-]")
            self.axis.set_ylabel("Distanz [m]")
            if xLim is not None:
                self.axis.set_xlim(xLim)
                self.axis.set_ylim(yLim)
            self.axis.legend([found, lost], ["found at", "lost at"])

            # plt.title(f"{trackletThatGotLost}   " + r"$\theta$" + f" = {self.overlapThreshold}")
            # plt.title(f"{trackletThatGotLost}")
            self.figure.set_figwidth(4)
            self.figure.set_figheight(4)

            # plt.rcParams.update(
            #     {
            #         "text.usetex": True,
            #         "font.family": "Helvetica"
            #     }
            # )
            if self.save:
                self.figure.savefig(f"fresh/{trackletThatGotLost}_{self.overlapThreshold}.pdf",
                                    format="pdf", bbox_inches="tight")
            else:
                plt.show()

            plt.cla()
        plt.close()

    def plotLostAndFoundTrackletsDistance(self):
        x = []
        xtickLabels = []
        lostTracklets, foundTracklets = [], []

        for i in range(9):
            x.append(i)
            xtickLabels.append(self.distanceClasses[i])

        for _, row in self.lostDf.groupby("distanceClass", as_index=False).count().iterrows():
            lostTracklets.append(row.ID)

        for _, row in self.foundDf.groupby("distanceClass", as_index=False).count().iterrows():
            foundTracklets.append(row.ID)

        iusLost = InterpolatedUnivariateSpline(x, lostTracklets)
        iusFound = InterpolatedUnivariateSpline(x, foundTracklets)

        yLost = iusLost(x)
        yFound = iusFound(x)

        self.axis.plot(x, yLost, "k--")
        self.axis.plot(x, yFound, "k--")

        lost = self.axis.scatter(x=x, y=lostTracklets, c="r", marker="x")
        found = self.axis.scatter(x=x, y=foundTracklets, c="b", marker="o")

        self.axis.set_xticks(x)
        self.axis.set_xticklabels(xtickLabels)
        self.axis.set_xlabel("Distanz [m]")
        self.axis.set_ylabel("Tracklets [-]")
        self.axis.legend([found, lost], ["found at", "lost at"])

        self.figure.savefig("Gefundene_Verlorene_Tracklets_Distanz.svg")

    def plotFoundTrackletsDistance(self, save=True):
        self.save = save

        x = []
        xtickLabels = []
        foundTracklets = []
        df = self.foundDf.groupby("distanceClass", as_index=False).count()
        for _, row in df.iterrows():
            foundTracklets.append(row.ID)

        for i in range(len(foundTracklets)):
            x.append(i)
            xtickLabels.append(self.distanceClasses[i])

        iusFound = InterpolatedUnivariateSpline(x, foundTracklets)
        yFound = iusFound(x)

        self.axis.plot(x, yFound, "k--")

        found = self.axis.scatter(x=x, y=foundTracklets, c="b", marker="o")

        self.axis.set_xticks(x)
        self.axis.set_xticklabels(xtickLabels)
        self.axis.set_xlabel("Distanz [m]")
        self.axis.set_ylabel("Tracklets [-]")
        self.axis.legend([found], ["found at"])

        plt.title("Gefundene Tracklets   " + r"$\theta$" + f" = {self.overlapThreshold}")
        if self.save:
            self.figure.savefig(
                f"Gefundene_Tracklets_Distanz_{self.overlapThreshold}.pdf",
                format="pdf", bbox_inches="tight"
            )
        else:
            plt.show()

    def plotLostTrackletsDistance(self, save=True):
        self.save = save

        x = []
        xtickLabels = []
        lostTracklets = []

        df = self.lostDf.groupby("distanceClass", as_index=False).count()
        for _, row in df.iterrows():
            lostTracklets.append(row.ID)

        for i in range(len(lostTracklets)):
            x.append(i)
            xtickLabels.append(self.distanceClasses[i])

        iusLost = InterpolatedUnivariateSpline(x, lostTracklets)
        yLost = iusLost(x)

        self.axis.plot(x, yLost, "k--")

        lost = self.axis.scatter(x=x, y=lostTracklets, c="r", marker="x")

        self.axis.set_xticks(x)
        self.axis.set_xticklabels(xtickLabels)
        self.axis.set_xlabel("Distanz [m]")
        self.axis.set_ylabel("Tracklets [-]")
        self.axis.legend([lost], ["lost at"])

        plt.title("Verlorene Tracklets   " + r"$\theta$" + f" = {self.overlapThreshold}")
        if self.save:
            self.figure.savefig(
                f"Verlorene_Tracklets_Distanz_{self.overlapThreshold}.pdf",
                format="pdf", bbox_inches="tight"
            )
        else:
            plt.show()


    def plotLostTrackletsDistanceIntoAxis(self, axis):
        x = []
        xtickLabels = []
        lostTracklets = []

        for i in range(9):
            x.append(i)
            xtickLabels.append(self.distanceClasses[i])
        for _, row in self.lostDf.groupby("distanceClass", as_index=False).count().iterrows():
            lostTracklets.append(row.ID)

        iusLost = InterpolatedUnivariateSpline(x, lostTracklets)
        yLost = iusLost(x)

        axis.plot(x, yLost, "k--")

        lost = axis.scatter(x=x, y=lostTracklets, c="r", marker="x")

        axis.set_xticks(x)
        axis.set_xticklabels(xtickLabels)
        axis.set_xlabel("Distanz [m]")
        axis.set_ylabel("Tracklets [-]")
        axis.legend([lost], ["lost at"])
        plt.title("Verlorene Tracklets   " + r"$\theta$" + f" = {self.overlapThreshold}")

    def plotTransitionsDistance(self, save=True):
        self.save = save


        x = []
        xtickLabels = []
        transitions = [0] * 10



        for i in range(len(transitions)):
            x.append(i)
            xtickLabels.append(self.distanceClasses[i])

        for i, row in self.lostDf.groupby("distanceClass", as_index=False).count().iterrows():
            transitions[i] = transitions[i] + row.ID

        for i, row in self.foundDf.groupby("distanceClass", as_index=False).count().iterrows():
            transitions[i] = transitions[i] + row.ID

        ius = InterpolatedUnivariateSpline(x, transitions)
        y = ius(x)

        self.axis.plot(x, y, "k--")

        transition = self.axis.scatter(x=x, y=transitions, c="m", marker="v")

        self.axis.set_xticks(x)
        self.axis.set_xticklabels(xtickLabels)
        self.axis.set_xlabel("Distanz [m]")
        self.axis.set_ylabel("Tracklets [-]")
        self.axis.legend([transition], ["transition"])

        plt.title("Transitionen Tracklets   " + r"$\theta$" + f" = {self.overlapThreshold}")
        if self.save:
            self.figure.savefig(
                f"Transitionen_Distanz_{self.overlapThreshold}.pdf",
                format="pdf", bbox_inches="tight"
            )
        else:
            plt.show()

    def plotRelativeFrequencyTransitions(self, save=True):
        self.save = save

        transitionsDistanceClass = []
        for ID in self.trackletsThatGotLost:
            trackletAnalyser = self.trackletAnalysers.get(ID)
            for distanceClass in trackletAnalyser.foundAtDistanceClass:
                transitionsDistanceClass.append(distanceClass)
            for distanceClass in trackletAnalyser.lostAtDistanceClass:
                transitionsDistanceClass.append(distanceClass)

        x = []
        xtickLabels = []

        for i in range(8):
            x.append(i)
            xtickLabels.append(self.distanceClasses[i])

        relativeFrequency = stats.relfreq(transitionsDistanceClass, 8)
        x = relativeFrequency.lowerlimit + np.linspace(
            0, relativeFrequency.binsize * relativeFrequency.frequency.size, relativeFrequency.frequency.size
        )
        a = relativeFrequency.frequency
        self.axis.bar(x, relativeFrequency.frequency, width=7, color="m")
        self.axis.set_xticks(x)
        self.axis.set_xticklabels(xtickLabels)
        self.axis.set_xlabel("Distanz [m]")
        self.axis.set_ylabel("Relative Häufigkeit [-]")

        # plt.title("Relative Häufigkeit Transitionen Tracklets   " + r"$\theta$" + f" = {self.overlapThreshold}")
        if self.save:
            self.figure.savefig(
                f"Frequenz_Transitionen_Distanz_{self.overlapThreshold}.pdf",
                format="pdf", bbox_inches="tight"
            )
        else:
            plt.show()


    def plotRelativeFrequencyLost(self, save=True):
        self.save = save

        lostAtDistanceClass = []
        for ID in self.trackletsThatGotLost:
            trackletAnalyser = self.trackletAnalysers.get(ID)
            for distanceClass in trackletAnalyser.foundAtDistanceClass:
                lostAtDistanceClass.append(distanceClass)

        x = []
        xtickLabels = []
        for i in range(8):
            x.append(i)
            xtickLabels.append(self.distanceClasses[i])

        relativeFrequency = stats.relfreq(lostAtDistanceClass, 8)
        x = relativeFrequency.lowerlimit + np.linspace(
            0, relativeFrequency.binsize * relativeFrequency.frequency.size, relativeFrequency.frequency.size
        )
        a = relativeFrequency.frequency
        self.axis.bar(x, relativeFrequency.frequency, width=7, color="r")
        self.axis.set_xticks(x)
        self.axis.set_xticklabels(xtickLabels)
        self.axis.set_xlabel("Distanz [m]")
        self.axis.set_ylabel("Relative Häufigkeit [-]")

        plt.title("Relative Häufigkeit Verlorener Tracklets   " + r"$\theta$" + f" = {self.overlapThreshold}")
        if self.save:
            # self.figure.savefig(
            #     f"Frequenz_Verlorene_Distanz_{self.overlapThreshold}.pdf",
            #     format="pdf", bbox_inches="tight"
            # )
            self.figure.savefig(
                f"Frequenz_Verlorene_Distanz_{self.overlapThreshold}.svg", bbox_inches="tight"
            )
        else:
            plt.show()


    def plotRelativeFrequencyFound(self, save=True):
        self.save = save

        foundAtDistanceClass = []
        for ID in self.trackletsThatGotLost:
            trackletAnalyser = self.trackletAnalysers.get(ID)
            for distanceClass in trackletAnalyser.foundAtDistanceClass:
                foundAtDistanceClass.append(distanceClass)

        x = []
        xtickLabels = []
        for i in range(8):
            x.append(i)
            xtickLabels.append(self.distanceClasses[i])

        relativeFrequency = stats.relfreq(foundAtDistanceClass, 8)
        x = relativeFrequency.lowerlimit + np.linspace(
            0, relativeFrequency.binsize * relativeFrequency.frequency.size, relativeFrequency.frequency.size
        )
        a = relativeFrequency.frequency
        iusLost = InterpolatedUnivariateSpline(x, relativeFrequency.frequency)
        yLost = iusLost(x)

        # self.axis.plot(x, yLost, "k--")


        self.axis.bar(x, relativeFrequency.frequency, width=7, color="b")
        self.axis.set_xticks(x)
        self.axis.set_xticklabels(xtickLabels)
        self.axis.set_xlabel("Distanz [m]")
        self.axis.set_ylabel("Relative Häufigkeit [-]")

        plt.title("Relative Häufigkeit Gefundener Tracklets   " + r"$\theta$" + f" = {self.overlapThreshold}")
        if self.save:
            # self.figure.savefig(
            #     f"Frequenz_Gefundene_Distanz_{self.overlapThreshold}.pdf",
            #     format="pdf", bbox_inches="tight"
            # )
            self.figure.savefig(
                f"Frequenz_Gefundene_Distanz_{self.overlapThreshold}.svg", bbox_inches="tight"
            )
        else:
            plt.show()

    def __buildDataFrame(self):
        lostID, foundID = [], []
        lostImageIndex, foundImageIndex = [], []
        lostArea, foundArea = [], []
        lostDistance, foundDistance = [], []
        lostDistanceClass, foundDistanceClass = [], []

        for ID in self.trackletsThatGotLost:
            tracklet = self.trackletAnalysers.get(ID)
            self.__buildLists(0, ID, lostArea, lostDistance, lostDistanceClass, lostID, lostImageIndex, tracklet)
            self.__buildLists(1, ID, foundArea, foundDistance, foundDistanceClass, foundID, foundImageIndex, tracklet)

        self.lostDf = pd.DataFrame(
            {
                "ID": lostID,
                "imageIndex": lostImageIndex,
                "area": lostArea,
                "distance": lostDistance,
                "distanceClass": lostDistanceClass
            }
        )

        self.foundDf = pd.DataFrame(
            {
                "ID": foundID,
                "imageIndex": foundImageIndex,
                "area": foundArea,
                "distance": foundDistance,
                "distanceClass": foundDistanceClass
            }
        )

    @staticmethod
    def __buildLists(case, ID, area, distance, distanceClass, IDs, imageIndex, tracklet):
        if case == 0:
            for i in range(len(tracklet.lostAtImageIndex)):
                IDs.append(ID)
                area.append(tracklet.lostAtArea[i])
                imageIndex.append(tracklet.lostAtImageIndex[i])
                distance.append(tracklet.lostAtDistance[i])
                distanceClass.append(tracklet.lostAtDistanceClass[i])
        if case == 1:
            for i in range(len(tracklet.foundAtImageIndex)):
                IDs.append(ID)
                area.append(tracklet.foundAtArea[i])
                imageIndex.append(tracklet.foundAtImageIndex[i])
                distance.append(tracklet.foundAtDistance[i])
                distanceClass.append(tracklet.foundAtDistanceClass[i])

    @staticmethod
    def rel_freq(x):
        return [(value, x.count(value) / len(x)) for value in set(x)]




class CombiPlotter(EvaluationPlotter):
    def __init__(self, path, out, width=0.25, verbose=False, overlapThreshold="_COMBO.csv"):
        super().__init__(path, out, verbose, overlapThreshold)
        self.width = width

        self.__sortMatched()
        self.distanceClasses = (
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
        )

    def plotMatched(self):
        boxes = self.__buildBoxes()
        self.__plotBars(boxes)

        self.axis.set_xlabel("Distanz [m]")
        self.axis.set_ylabel("Boxen [-]")
        self.axis.legend(loc="upper right")
        plt.savefig(os.path.join(self.out, "Gefundene_Boxen_Distanz.svg"))

    def plotCoverageDistance(self):
        boxesDict = self.__buildBoxes()
        percentages = []
        io = []
        nio = []
        for boxes in boxesDict.get("io"):
            io.append(boxes)

        for boxes in boxesDict.get("nio"):
            nio.append(boxes)

        total = []
        for i in range(10):
            total.append(io[i] + nio[i])
            percentages.append(io[i] / total[i] * 100)

        mean = np.mean(percentages)
        x = np.arange(0, 100, 10)
        ius = InterpolatedUnivariateSpline(x, percentages)
        y = ius(x)

        self.axis.plot(x, y, "--")
        meanLine = self.axis.axhline(mean, c="k")
        scatter = self.axis.scatter(x, percentages)
        self.axis.set_xlabel("Distanz [m]")
        self.axis.set_ylabel("Abdeckung [%]")
        self.axis.set_xticks(x)
        self.axis.set_xticklabels(self.distanceClasses)
        self.axis.legend([meanLine, scatter], ["mean", "coverage"])
        plt.grid()
        # plt.show()
        plt.savefig(os.path.join(self.out, "Abdeckung_Distanz.svg"))

    def __buildBoxes(self):
        df = self.giantDataFrame.filter(
            items=[
                "overlap",
                "distance",
                "distanceClass",
                "matched"
            ]
        )
        df = df.groupby(["distanceClass", "matched"], as_index=False).count()

        io = [0] * 10
        nio = [0] * 10
        i, j = 0, 0

        for index, row in df.iterrows():
            if row.matched:
                io[i] = row.distance
                i = i + 1
            else:
                nio[j] = row.distance
                j = j + 1
        boxes = {
            "io": io,
            "nio": nio
        }
        return boxes

    def __plotBars(self, boxes: dict):
        bottom = np.zeros(10)

        for matched, boxes in boxes.items():
            self.axis.bar(self.distanceClasses, boxes, self.width, label=matched, bottom=bottom)
            bottom += boxes
