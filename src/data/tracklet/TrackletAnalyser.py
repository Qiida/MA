class TrackletAnalyser:

    def __init__(self, df):

        self.ID = None
        self.found = []
        self.foundFrame = []
        self.lost = []
        self.lostFrame = []

        self.lostAtImageIndex = []
        self.lostAtArea = []
        self.lostAtDistance = []
        self.lostAtDistanceClass = []

        self.foundAtImageIndex = []
        self.foundAtArea = []
        self.foundAtDistance = []
        self.foundAtDistanceClass = []

        rows = []
        isOnTrack = []

        for i, (_, row) in enumerate(df.iterrows()):
            rows.append(row)

            if self.ID is None:
                self.ID = row.ID

            if row.matched:
                isOnTrack.append(True)

                self.found.append(row.distance)
                self.foundFrame.append(row.imageIndex)
                self.__appendFoundAtLists(i, row, isOnTrack)

            if not row.matched:
                isOnTrack.append(False)

                self.lost.append(row.distance)
                self.lostFrame.append(row.imageIndex)
                self.__appendLostAtLists(i, rows, isOnTrack)

        if len(self.found) == 0:
            self.lost = []

    def __appendLostAtLists(self, i, rows, isOnTrack):
        if i > 0:
            if isOnTrack[i - 1]:
                self.lostAtImageIndex.append(rows[i - 1].imageIndex)
                self.lostAtArea.append(rows[i - 1].k_area)
                self.lostAtDistance.append(rows[i - 1].distance)
                self.lostAtDistanceClass.append(rows[i - 1].distanceClass)
        if i == 0:
            if not isOnTrack[i]:
                self.lostAtImageIndex.append(rows[i].imageIndex)
                self.lostAtArea.append(rows[i].k_area)
                self.lostAtDistance.append(rows[i].distance)
                self.lostAtDistanceClass.append(rows[i].distanceClass)

    def __appendFoundAtLists(self, i, row, isOnTrack):
        if i > 0:
            if not isOnTrack[i - 1]:
                self.foundAtImageIndex.append(row.imageIndex)
                self.foundAtArea.append(row.k_area)
                self.foundAtDistance.append(row.distance)
                self.foundAtDistanceClass.append(row.distanceClass)
        if i == 0:
            if isOnTrack[i]:
                self.foundAtImageIndex.append(row.imageIndex)
                self.foundAtArea.append(row.k_area)
                self.foundAtDistance.append(row.distance)
                self.foundAtDistanceClass.append(row.distanceClass)
