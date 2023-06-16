import matplotlib

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from PyQt5.Qt import Qt
from PyQt5.QtWidgets import QMainWindow

from resources.QtDesign.windowMain import Ui_MainWindow
from src.app.CPointMatcher.Annotation import AnnotationStyle

matplotlib.use("Qt5Agg")


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, correspondencePointMatcher):
        super().__init__()
        self.setupUi(self)
        self.cpm = correspondencePointMatcher

        self.button04.clicked.connect(self.clickButton04)
        self.button15.clicked.connect(self.clickButton15)
        self.button26.clicked.connect(self.clickButton26)
        self.button37.clicked.connect(self.clickButton37)

    def clickButton04(self):
        self.writeInFile(0)

    def clickButton15(self):
        self.writeInFile(1)

    def clickButton26(self):
        self.writeInFile(2)

    def clickButton37(self):
        self.writeInFile(3)

    def writeInFile(self, vertex):

        ID = self.lineEdit.text()
        print("LidarObject ID: {}".format(ID))
        print("Vertex: {}".format(vertex))
        point = self.cpm.getPointOfInterest()
        print(point)
        self.cpm.outputFile.write("\n")


        newLine = str(self.cpm.frames[self.cpm.frameIndex].frameNr) + self.cpm.seperator + str(point[0]) + self.cpm.seperator + \
                  str(point[1]) + self.cpm.seperator + str(self.cpm.frames[self.cpm.frameIndex].idNr) + \
                  self.cpm.seperator + ID + self.cpm.seperator + str(vertex)

        self.cpm.outputFile.write(newLine)
        print("Add new Line: {}".format(newLine))

    def keyPressEvent(self, event):

        if event.key() == Qt.Key_W:
            self.cpm.pointIndex += 1
            if self.cpm.pointIndex > 3:
                self.cpm.pointIndex = 0
            self.resetAndPlot()

        if event.key() == Qt.Key_S:
            self.cpm.pointIndex -= 1
            if self.cpm.pointIndex < 0:
                self.cpm.pointIndex = 3
            self.resetAndPlot()

        if event.key() == Qt.Key_A:
            self.cpm.frameIndex -= 1
            if self.cpm.frameIndex < 0:
                self.cpm.frameIndex = len(self.cpm.frames) - 1

            try:
                self.resetAndPlot()
            except:
                print(self.cpm.frameIndex)

        if event.key() == Qt.Key_D:
            self.cpm.frameIndex += 1
            if self.cpm.frameIndex > len(self.cpm.frames) - 1:
                self.cpm.frameIndex = 0

            try:
                self.resetAndPlot()
            except:
                print(self.cpm.frameIndex)

        if event.key() == Qt.Key_C:
            self.cpm.annotationIndex += 1
            print(self.cpm.annotationIndex)
            print(len(self.cpm.frames[self.cpm.frameIndex].annotations))
            if self.cpm.annotationIndex > len(self.cpm.frames[self.cpm.frameIndex].annotations) - 1:
                self.cpm.annotationIndex = 0
            self.resetAndPlot()

        if event.key() == Qt.Key_F5:
            self.close()

    def resetAndPlot(self):
        self.cpm.resetAxes()
        self.cpm.draw()
        self.cpm.figure.canvas.draw()


class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, figure):
        super(MplCanvas, self).__init__(figure=figure)
