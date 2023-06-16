def buildShortName(dataSetName):
    splits = dataSetName.split("_")
    return splits[0][2:] + splits[1] + splits[2] + "_" + splits[4]
