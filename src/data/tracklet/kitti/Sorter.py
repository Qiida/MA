class TrackletSorter:
    def __init__(self, tracklets):
        self.tracklets = tracklets
        self.sortedBoxes = {
            0: [],
            10: [],
            20: [],
            30: [],
            40: [],
            50: [],
            60: [],
            70: [],
            80: [],
            90: []
        }

        self.__sortBoxes(tracklets)

    def __sortBoxes(self, tracklets):
        for tracklet in tracklets:
            for box in tracklet.boxes:
                if 0 < box.distance < 10:
                    self.sortedBoxes.get(0).append(box)
                if 10 < box.distance < 20:
                    self.sortedBoxes.get(10).append(box)
                if 20 < box.distance < 30:
                    self.sortedBoxes.get(20).append(box)
                if 30 < box.distance < 40:
                    self.sortedBoxes.get(30).append(box)
                if 40 < box.distance < 50:
                    self.sortedBoxes.get(40).append(box)
                if 50 < box.distance < 60:
                    self.sortedBoxes.get(50).append(box)
                if 60 < box.distance < 70:
                    self.sortedBoxes.get(60).append(box)
                if 70 < box.distance < 80:
                    self.sortedBoxes.get(70).append(box)
                if 80 < box.distance < 90:
                    self.sortedBoxes.get(80).append(box)
                if 90 < box.distance:
                    self.sortedBoxes.get(90).append(box)

